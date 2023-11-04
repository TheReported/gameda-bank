from django.urls import path

from . import views

app_name = 'bank_account'
urlpatterns = [
    path('', views.display, name='display'),
    path('create/', views.create, name='create'),
]
