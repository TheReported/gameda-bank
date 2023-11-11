from django.urls import path

from . import views

app_name = 'bank_account'
urlpatterns = [
    path('', views.display, name='display'),
    path('create/', views.create, name='create'),
    path('create/done', views.create_done, name='create_done'),
    path('<code>/', views.detail, name='bank_account_detail'),
    path('<code>/edit/', views.edit, name='bank_account_edit'),
]
