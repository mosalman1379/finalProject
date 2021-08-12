import datetime
import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from sale.models import FollowUp
from products.models import Manufacture_Product
from organization.models import Organization
from organization.forms import OrganizationForm
from organization.serializer import OrganizationSerializer
from organization.permission import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class CreateOrganization(LoginRequiredMixin, CreateView):
    """
    create organization view
    """
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
    """
    list all organization that self user created
    """
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
        kwargs['reports'] = FollowUp.objects.all()[:3]
        products_tags = set(
            map(lambda x: x.tags.values_list('id', flat=True), self.object.production_crop.all()))
        #  change recommended via tags
        try:
            kwargs['recommended'] = list(
                map((lambda x: x[1]), list(Manufacture_Product.objects.filter(tags__in=products_tags).exclude(
                    pk=kwargs['object'].id).values_list())))
        except TypeError:
            kwargs['recommended'] = ''
        # pk user
        kwargs['pk'] = self.object.registrant_user.pk
        return super(OrganizationDetail, self).get_context_data(**kwargs)


class OrganizationEdit(LoginRequiredMixin, UpdateView):
    """
    Edit each organization
    """
    template_name = 'organization/edit.html'
    model = Organization
    fields = ('province', 'organization_name', 'organization_phone',
              'workers', 'contact_fullname',
              'contact_mobile', 'email', 'status')
    success_url = reverse_lazy('organization:list')

    def get_object(self, queryset=None):
        return super(OrganizationEdit, self).get_object(queryset)


class OrganizationViewSet(LoginRequiredMixin, ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
