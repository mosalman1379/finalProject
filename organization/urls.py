from django.urls import path
from organization.views import CreateOrganization, OrganizationList, OrganizationDetail, OrganizationEdit
from django.contrib.auth import views as auth_view
app_name = 'organization'
urlpatterns = [
    path('create/', CreateOrganization.as_view(), name='create'),
    path('all/',OrganizationList.as_view(),name='list'),
    path('detail/<int:pk>/',OrganizationDetail.as_view(),name='detail'),
    path('edit/<int:pk>/',OrganizationEdit.as_view(),name='edit'),
]
