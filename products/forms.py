from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'taxable',
                  'catalog_pdf', 'catalog_image', 'description',
                  'manufacture_products')
        widgets = {
            'taxable': forms.CheckboxInput,
        }

    def clean_catalog_image(self):
        catalog_image = self['catalog_image'].data.name
        if catalog_image.endswith('.jpg') or catalog_image.endswith('.jpeg'):
            return catalog_image
        raise forms.ValidationError('invalid file extension(only jpg or jpeg)')

    def clean_catalog_pdf(self):
        catalog_pdf=self['catalog_pdf'].data.name
        if catalog_pdf.endswith('.pdf'):
            return catalog_pdf
        raise forms.ValidationError('invalid file extension (only pdf)')
