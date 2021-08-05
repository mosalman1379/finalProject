from django import forms
from products.models import Product


# product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'taxable',
                  'catalog_pdf', 'catalog_image', 'description',
                  'manufacture_products')
        widgets = {
            'taxable': forms.CheckboxInput,
        }

    # checking validation of image file
    def clean_catalog_image(self):
        x = 1
        catalog_image = str(self['catalog_image'].initial)
        if catalog_image.endswith('.jpg') or catalog_image.endswith('.jpeg'):
            return catalog_image
        raise forms.ValidationError('invalid file extension(only jpg or jpeg)')

    # checking validation of pdf file
    def clean_catalog_pdf(self):
        x = 1
        catalog_pdf = str(self['catalog_pdf'].initial)
        if catalog_pdf.endswith('.pdf'):
            return catalog_pdf
        raise forms.ValidationError('invalid file extension (only pdf)')
