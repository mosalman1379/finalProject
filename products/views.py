from django.conf import settings
from django.http import HttpResponse, FileResponse

from products.models import Product


def download_catalog(request, pk):
    obj=Product.objects.get(pk=pk)
    filename=obj.catalog_pdf.name
    path=str(settings.MEDIA_ROOT)+'/'+filename
    response=FileResponse(open(path,'rb'),content_type='application/pdf')
    response['Content-Disposition']="attachment; filename=%s" % filename[5:]
    return response
