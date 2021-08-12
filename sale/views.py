import datetime
import json
from smtplib import SMTPException
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from my_signal import email_signal
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView, ListView, DetailView
from sale.models import Quote, FollowUp, QuoteItem
from products.models import Product
from sale.forms import QuoteItemForm, ReportForm
from organization.models import Organization
import weasyprint
from sale.celery_tasks import send_mail_to


class CreateQuote(LoginRequiredMixin, FormView):
    form_class = QuoteItemForm
    template_name = 'sale/create.html'
    """
    Create Quote class based view 
    """
    def get_context_data(self, **kwargs):
        kwargs['products'] = Product.objects.all().values_list()
        kwargs['organizations'] = Organization.objects.all().values_list()
        return super(CreateQuote, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        content = request.POST.get('contents', None)
        data = json.loads(content)
        quote = Quote.objects.create(organization_id=int(data[0]['organizationId']), quote_date=datetime.datetime.now())
        for item in data:
            QuoteItem.objects.create(device_id=int(item['deviceId']), quantity=int(item['quantity']),
                                     price=int(item['price']), discount=float(item['discount']) / 100.0,
                                     quote_id=quote.pk)
        return JsonResponse(data={'message': 'Quote saved successfully'}, status=200)


class QuoteList(LoginRequiredMixin, ListView):
    paginate_by = 3
    template_name = 'sale/list.html'
    model = Quote
    """
    list quote items class based view 
    """


class PrintOrder(LoginRequiredMixin, DetailView):
    model = Quote
    """
    get pdf output file of quote
    """
    def get(self, request, *args, **kwargs):
        g = super(PrintOrder, self).get(request, *args, **kwargs)
        rendered_content = g.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response


# describe each report
class Report_detail(LoginRequiredMixin,DetailView):
    template_name = 'sale/detail_report.html'

    def get_object(self, queryset=None):
        return FollowUp.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        kwargs['report']=self.get_object()
        return super(Report_detail, self).get_context_data(**kwargs)

@require_POST
def save_report(request):
    """
    save report on organization page
    """
    report = request.POST.get('report', None)
    user_pk = int(request.POST.get('user_pk', None))
    user = User.objects.get(pk=user_pk)
    form_instance = ReportForm({'user': user, 'date': datetime.datetime.now(), 'report': report})
    if form_instance.is_valid():
        form_instance.save()
        return JsonResponse(data={'status': 'ok', 'message': 'Report saved successfully'}, status=200)
    else:
        return JsonResponse(data={'status': 'error', 'message': "Report doesn't saved successfully"}, status=400)


# sending email by class based view
class Email_send(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        quote = Quote.objects.get(pk=kwargs['pk'])
        organization_email = quote.organization.email
        quotes = quote.quoteitem_set.all()
        try:
            send_mail_to('CRM Email', 'sale/email.html', organization_email, quotes)
            email_signal.send(sender=Quote, instance=quote, success=True)
            messages.info(request, 'email sent!')
        except SMTPException:
            email_signal.send(sender=Quote, instance=quote, success=False)
        return redirect('sale:list')
