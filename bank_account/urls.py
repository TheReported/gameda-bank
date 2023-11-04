from django.urls import path

from . import views

urlpatterns = [
    path('bank_account/', views.create_bank_account, name='init'),
]
