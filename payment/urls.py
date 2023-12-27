from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.display_payment, name='display'),
    path('done/', views.payment_done, name='done'),
    path('proccess/', views.payment_proccess, name='proccess'),
    path('<int:payment_id>/pdf/', views.payment_pdf, name='pdf'),
]
