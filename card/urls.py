from django.urls import path

from . import views

app_name = "card"

urlpatterns = [
    path('', views.display_card, name="display"),
    path('create/', views.create, name='create'),
    path('create/done', views.create_done, name='create_done'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/edit/', views.edit, name='edit'),
]
