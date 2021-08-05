from django import forms
from sale.models import FollowUp
from products.models import Product
from organization.models import Organization


class QuoteItemForm(forms.Form):
    organ=forms.ModelChoiceField(queryset=Organization.objects.all(),initial='')
    device=forms.ModelChoiceField(queryset=Product.objects.all())
    quantity=forms.IntegerField()
    price=forms.IntegerField()
    discount=forms.FloatField()


class ReportForm(forms.ModelForm):
    class Meta:
        model=FollowUp
        fields=('user','report')
