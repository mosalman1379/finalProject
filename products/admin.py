import logging
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from taggit.models import Tag
from products.forms import ProductForm
from products.models import Product, Manufacture_Product

logger = logging.getLogger(__name__)


@admin.register(Product)
class Product(admin.ModelAdmin):
    # this attribute change display of add or change form in admin
    fields = (('name', 'price', 'taxable'), 'catalog_pdf', 'catalog_image', 'description', 'manufacture_products')
    form = ProductForm
    change_form_template = 'admin/product_add.html'
    # pagination in admin django
    list_per_page = 3
    list_display = ('name','price','taxable','download_link')


@admin.register(Manufacture_Product)
class ManufactureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    add_form_template = 'admin/manufacture_add.html'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context=extra_context or {}
        extra_context['tags']=Tag.objects.all().values_list()
        return super(ManufactureAdmin, self).add_view(request, form_url, extra_context)
