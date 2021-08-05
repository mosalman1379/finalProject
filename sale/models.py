from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum
from django.urls import reverse

from organization.models import Organization
from products.models import Product
from django.utils.translation import ugettext_lazy as _


class QuoteItem(models.Model):
    device = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Device'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Device quantity'))
    price = models.PositiveBigIntegerField(verbose_name=_('device price'))
    discount = models.FloatField(default=0, verbose_name=_('Device discount'))
    quote = models.ForeignKey('sale.Quote', on_delete=models.CASCADE, null=True)

    def output_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Quote Item with total price {self.output_price()}'


class Quote(models.Model):
    """
    Quote model fields
    """
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.organization} quote'
    #
    # def get_total_grand(self):
    #     return self.quoteItems.all().aggregate(Sum('total_price'))


class FollowUp(models.Model):
    """
    Follow up model
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('user'))
    date = models.DateTimeField(verbose_name=_('Date'), auto_now=True)
    report = models.TextField(verbose_name=_('report'))

    def __str__(self):
        return f'The report created in {self.date} by {self.user}'

    def format_time(self):
        return self.date.strftime('%Y-%m-%d')

    def get_absolute_url(self):
        return reverse('sale:report detail', args=[self.pk])
