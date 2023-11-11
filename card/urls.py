from django.urls import path

from . import views

app_name = "card"

urlpatterns = [
    path('', views.display_card, name="display"),
    path('create/', views.create, name='create'),
    path('create/done', views.create_done, name='create_done'),
    path('<code>/', views.detail, name='detail'),
    path('<code>/edit/', views.edit, name='edit'),
]
