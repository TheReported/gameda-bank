from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('activity/', views.activity, name='activity'),
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
]
