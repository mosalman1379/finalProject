from django.contrib import admin
from organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('province', 'registrant_user', 'contact_fullname', 'status')
    exclude = ('status','registrant_user','created_date')
    list_filter = ('province','production_crop','status')
    list_per_page = 3
