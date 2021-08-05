from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from products.models import Product, Manufacture_Product
from organization.enums import OrganizationStatus

organization_phone_regex = RegexValidator(regex='^0[0-9]+$', message='invalid organization phone number')

mobile_phone_regex = RegexValidator(regex='^09[0-9]{9}$', message='invalid mobile phone number')


# organization model

class Organization(models.Model):
    province = models.CharField(verbose_name=_('province'), max_length=20)
    organization_name = models.CharField(max_length=50, verbose_name=_('organization name'))
    organization_phone = models.CharField(validators=[organization_phone_regex], max_length=11)
    workers = models.PositiveIntegerField(default=1, verbose_name=_('workers count'))
    production_crop = models.ManyToManyField(Manufacture_Product, related_name='product_entry',
                                             verbose_name=_('production crop'))
    contact_fullname = models.CharField(max_length=100, verbose_name=_('contact full name'))
    contact_mobile = models.CharField(validators=[mobile_phone_regex], verbose_name=_('contact mobile number'),
                                      max_length=11)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    registrant_user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('registrant user'))
    status = models.CharField(choices=OrganizationStatus.choices, default=OrganizationStatus.in_progress, max_length=20)
    Followup = models.ForeignKey('sale.FollowUp', on_delete=models.PROTECT, verbose_name=_('Report'), null=True)

    # format time in created_date field
    def format_time(self):
        return self.created_date.strftime(format('%Y-%m-%d'))

    def __str__(self):
        return f'{self.organization_name} located in {self.province}'
