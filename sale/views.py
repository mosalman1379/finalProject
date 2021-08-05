import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
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

    def get_context_data(self, **kwargs):
        kwargs['products'] = Product.objects.all().values_list()
        kwargs['organizations'] = Organization.objects.all().values_list()
        return super(CreateQuote, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        price = int(request.POST.get('price', None))
        discount = float(request.POST.get('discount', None))
        quantity = int(request.POST.get('quantity', None))
        organ = int(request.POST.get('organ', None))
        device = int(request.POST.get('device', None))
        u = Quote(organization_id=organ)
        u.save()
        x = QuoteItem(price=price, discount=discount, quantity=quantity,device_id=device,quote_id=u.pk)
        x.save()
        return redirect('sale:list')

    def form_invalid(self, form):
        messages.error(request=self.request, message='Your inputs are incorrect')
        return super(CreateQuote, self).form_invalid(form)


class QuoteList(LoginRequiredMixin, ListView):
    paginate_by = 3
    template_name = 'sale/list.html'
    model = Quote


class PrintOrder(LoginRequiredMixin, DetailView):
    model = Quote

    def get(self, request, *args, **kwargs):
        g = super(PrintOrder, self).get(request, *args, **kwargs)
        rendered_content = g.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response


def report_detail(request, pk):
    report = get_object_or_404(klass=FollowUp, pk=pk)
    return render(request, 'sale/detail_report.html', context={'report': report})


def save_report(request):
    report = request.GET.get('report', None)
    user_pk = request.GET.get('user_pk', None)
    user = User.objects.get(pk=user_pk)
    form_instance = ReportForm({'user': user, 'date': datetime.datetime.now(), 'report': report})
    if form_instance.is_valid():
        form_instance.save()
        return JsonResponse(data={'status': 'ok', 'message': 'report save successfully'}, status=200)
    else:
        return JsonResponse(data={'status': 'error', 'message': 'invalid data'}, status=400)


def email_order(request, pk):
    organ=Organization.objects.get(pk=pk)
    organization_email = organ.email
    quotes=Quote.objects.all().values_list()
    send_mail_to('celery', 'celery_message', organization_email,quotes)
    messages.info(request,'email sent!')
    return redirect('sale:list',)
