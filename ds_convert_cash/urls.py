from django.contrib import admin
from django.urls import path, include
from core.views.currency_views import (CurrencyExchangeView,
                        CurrencyValuesView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', CurrencyValuesView.as_view(), name='currency_values'),
    path('exchange/', CurrencyExchangeView.as_view(), name='currency_exchange'),
]
