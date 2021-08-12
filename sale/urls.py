from django.urls import path
from sale.views import CreateQuote, QuoteList, PrintOrder, save_report, Email_send, Report_detail

app_name = 'sale'
urlpatterns = [
    path('create/', CreateQuote.as_view(), name='create'),
    path('list/',QuoteList.as_view(),name='list'),
    path('print/<int:pk>/',PrintOrder.as_view(),name='print'),
    path('report/<int:pk>/',Report_detail.as_view(),name='report_detail'),
    path('save/',save_report,name='save report'),
    path('email/<int:pk>/',Email_send.as_view(),name='email')
    # path('email/',email_order,name='email')
]
