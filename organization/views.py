import datetime
import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from sale.models import FollowUp
from products.models import Manufacture_Product
from organization.models import Organization
from organization.forms import OrganizationForm

logger = logging.getLogger(__name__)

# create view
@method_decorator(csrf_exempt, name='dispatch')
class CreateOrganization(LoginRequiredMixin, CreateView):
    template_name = 'organization/create.html'
    form_class = OrganizationForm
    success_url = reverse_lazy('organization:list')

    def form_valid(self, form):
        # set user by request.user
        form.instance.registrant_user = self.request.user
        logger.info(msg=f'{self.request.user.username} create new organization')
        super(CreateOrganization, self).form_valid(form)
        return redirect('organization:list')

    def form_invalid(self, form):
        logger.error(msg=f'{self.request.user.username} entered invalid input for form')
        messages.error(request=self.request, message='your inputs for this form in invalid check it again!')
        return super(CreateOrganization, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        # formatted date for using in template
        kwargs['date'] = datetime.datetime.now().strftime(format('%Y-%m-%d'))
        # getting user for using in template
        kwargs['registrant_contact'] = self.request.user.username
        return super(CreateOrganization, self).get_context_data(**kwargs)


class OrganizationList(LoginRequiredMixin, ListView):
    template_name = 'organization/list.html'
    paginate_by = 3
    # only organization created by request.user
    def get_queryset(self):
        logger.info(msg='loading organization models successfully')
        return Organization.objects.filter(registrant_user=self.request.user)

# detail of each organization
class OrganizationDetail(LoginRequiredMixin, DetailView):
    template_name = 'organization/detail.html'
    model = Organization

    def get(self, request, *args, **kwargs):
        return super(OrganizationDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # all products
        kwargs['all_products'] = list(
            map((lambda x: x[1]), list(Manufacture_Product.objects.values_list())))
        # Manufacture_Product.objects.filter()
        # all products except own organizations
        kwargs['reports']=list(FollowUp.objects.all().values_list())[-3:]
        kwargs['recommended'] = list(
            map((lambda x: x[1]), list(Manufacture_Product.objects.exclude(pk=kwargs['object'].id).values_list())))
        return super(OrganizationDetail, self).get_context_data(**kwargs)

# edit organization
class OrganizationEdit(LoginRequiredMixin, UpdateView):
    template_name = 'organization/edit.html'
    model = Organization
    fields = ('province', 'organization_name', 'organization_phone',
              'workers', 'contact_fullname',
              'contact_mobile', 'email', 'status')
    success_url = reverse_lazy('organization:list')

    def get_object(self, queryset=None):
        return super(OrganizationEdit, self).get_object(queryset)