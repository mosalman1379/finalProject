import logging

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

# manufacture model
class Manufacture_Product(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('product name'))

    def __str__(self):
        return self.name

# product model
class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('product name'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    taxable = models.BooleanField(default=True, verbose_name=_('taxable'))
    catalog_pdf = models.FileField(upload_to='pdfs/', verbose_name=_('pdf catalog'))
    catalog_image = models.FileField(upload_to='images/', verbose_name=_('image catalog'))
    description = models.TextField(blank=True)
    manufacture_products = models.ManyToManyField(Manufacture_Product, related_name='manufacture')
    number_of_devices = models.PositiveIntegerField(default=1)
    # total price of produc
    def total_price(self):
        return self.price * self.number_of_devices
    # adding a tag in admin django
    @admin.display(ordering='description')
    def download_link(self):
        return format_html('<a href="{0}" >DOWNLOAD</a>', reverse('products:download',args=[self.pk]))

    def __str__(self):
        return f'{self.name} with {self.price}$'
