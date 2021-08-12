from rest_framework import serializers
from organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    # Serializer class for organization model
    class Meta:
        model=Organization
        fields=('province','organization_name',
                'organization_phone','contact_fullname',
                'contact_mobile')


