from django.urls import path

from . import views

app_name = "card"

urlpatterns = [
    path('', views.display_card, name="init"),
]
