from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum, Count
from django.urls import reverse
from django.utils.functional import cached_property
from organization.models import Organization
from products.models import Product
from django.utils.translation import ugettext_lazy as _


class QuoteItem(models.Model):
    device = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Device'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Device quantity'))
    price = models.PositiveBigIntegerField(verbose_name=_('device price'))
    discount = models.FloatField(default=0, verbose_name=_('Device discount'))
    quote = models.ForeignKey('sale.Quote', on_delete=models.CASCADE, null=True)

    @cached_property
    def get_price(self):
        if self.device.taxable:
            total_without_discount = self.quantity * self.price * 1.09
            return self.discount * total_without_discount
        else:
            return self.discount * self.quantity * self.price

    def __str__(self):
        return f'Quote Item with total price {self.price * self.quantity}'


class Quote(models.Model):
    """
    Quote model fields
    """
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)
    quote_date = models.DateTimeField(verbose_name=_('Quote date'), auto_now=True)

    def __str__(self):
        return f'{self.organization} quote'

    @cached_property
    def get_total_price(self):
        return self.quoteitem_set.annotate(total=F('price') * F('quantity')).aggregate(Sum('total'))['total__sum']

    @cached_property
    def get_total_count(self):
        return self.quoteitem_set.aggregate(Count('quantity'))['quantity__count']


class FollowUp(models.Model):
    """
    Follow up model
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('user'))
    date = models.DateTimeField(verbose_name=_('Date'), auto_now=True)
    report = models.TextField(verbose_name=_('report'))

    class Meta:
        ordering=('-date',)

    def __str__(self):
        return f'The report created in {self.date} by {self.user}'

    @cached_property
    def format_time(self):
        return self.date.strftime('%Y-%m-%d')

    def get_absolute_url(self):
        return reverse('sale:report detail', args=[self.pk])


class EmailHistory(models.Model):
    email = models.EmailField(verbose_name=_('receiver email'))
    success = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return f'Email sent to {self.email} successfully' if self.success else f"Email doesn't sent to {self.email}"
