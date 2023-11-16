from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('activity/', views.activity, name='activity'),
    path('edit/', views.edit, name='edit'),
    path('discharge/', views.discharge, name='discharge'),
    path('register/', views.register, name='register'),
    path('bank_account/', include('bank_account.urls'), name='bank_account'),
    path('payment/', include('payment.urls'), name='payment'),
    path("card/", include("card.urls"), name="card"),
    path('transaction/', include("transaction.urls"), name="transaction"),
]
