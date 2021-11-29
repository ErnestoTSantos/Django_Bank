from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checking/', views.CheckingView.as_view(), name='checking'),
    path('saving/', views.SavingsView.as_view(), name='saving'),
    path('juridical/', views.JuridicalView.as_view(), name='juridical'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('details/', views.DetailsView.as_view(), name='details'),
]