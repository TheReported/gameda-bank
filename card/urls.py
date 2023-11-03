from django.urls import path

from . import views

urlpatterns = [path('card/<card_id>/', views.card_detail, name='card_detail')]
