from django.urls import path
from sale.views import CreateQuote, QuoteList, PrintOrder, report_detail, save_report, email_order

app_name = 'sale'
urlpatterns = [
    path('create/', CreateQuote.as_view(), name='create'),
    path('list/',QuoteList.as_view(),name='list'),
    path('print/<int:pk>/',PrintOrder.as_view(),name='print'),
    path('report/<int:pk>/',report_detail,name='report detail'),
    path('save/',save_report,name='save report'),
    path('email/<int:pk>/',email_order,name='email')
    # path('email/',email_order,name='email')
]
