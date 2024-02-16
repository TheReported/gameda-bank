"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from account import views as acc_views
from payment import views as payment_views
from transaction import views as transaction_views

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('user/', include('account.urls')),
    path('', acc_views.show_main, name='main'),
    path('payment/', payment_views.payment_curl_proccess, name='payment_curl_proccess'),
    path('rosetta/', include('rosetta.urls')),
)

urlpatterns += [
    path('api/', include('bank.router', namespace='api')),
    path('transfer/incoming/', transaction_views.transaction_inconming_proccess, name='incoming'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
