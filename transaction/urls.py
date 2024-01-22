from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.display_transaction, name='display'),
    path('done/', views.transaction_done, name='done'),
    path('outgoing/', views.transaction_outgoing_proccess, name='outgoing'),
    path('<int:transaction_id>/pdf/', views.transaction_pdf, name='pdf'),
    path('<int:transaction_id>/csv/', views.transaction_csv, name='csv'),
    path('csv/', views.all_transaction_csv, name='all_csv'),
]
