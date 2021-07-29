from django.db import models
from organization.models import Organization
from products.models import Product
from sale.enums import QuoteStatus
from django.utils.translation import ugettext_lazy as _


class Quote(models.Model):
    """
    Quote model fields
    """
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=1)
    counts = models.PositiveIntegerField(verbose_name=_('count'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    discount = models.FloatField(verbose_name=_('discount'), default=0)

    def __str__(self):
        return f'{self.organization} quote'


class QuateItem(models.Model):
    items = models.ForeignKey(Quote, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Product, related_name='product_item')
    status = models.CharField(choices=QuoteStatus.choices, default=QuoteStatus.waiting, max_length=20)

    def __str__(self):
        return f'Quote Item with pk:{self.pk}'
