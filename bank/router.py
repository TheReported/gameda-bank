from django.urls import include, path
from rest_framework import routers

from bank_account.api import views as bankapiviews
from card.api import views as cardapiviews
from transaction.api import views as transactionapiviews

app_name = 'router'

router = routers.DefaultRouter()
router.register('accounts', bankapiviews.BankAccountViewSet, basename='accounts')
router.register('cards', cardapiviews.CardViewSet, basename='cards')
router.register('transactions', transactionapiviews.TransactionViewSet, basename='transactions')


urlpatterns = [
    path('', include(router.urls)),
]
