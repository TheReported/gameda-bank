from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.show_main, name='main'),
    path('activity/', views.activity, name='activity'),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('', include('bank_account.urls'), name='bank_account'),
]
