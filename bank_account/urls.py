from django.urls import path

from . import views

app_name = 'bank_account'
urlpatterns = [
    path('', views.display, name='display'),
    path('create/', views.create, name='create'),
    path('create/done', views.create_done, name='create_done'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/edit/', views.edit, name='edit'),
]
