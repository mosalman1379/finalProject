from django import forms
from organization.models import Organization


# edit organization form
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('province', 'organization_name', 'organization_phone',
                  'workers', 'production_crop', 'contact_fullname', 'contact_mobile',
                  'email')
        widgets = {
            'email': forms.EmailInput,
            'workers':forms.NumberInput
        }