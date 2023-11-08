from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.display_transaction, name='display'),
    path('done/', views.transaction_done, name='done'),
]
