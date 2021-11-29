from django.urls import path

from . import views

app_name = 'counts'

urlpatterns = [
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw')
]