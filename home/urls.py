from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('home/', views.HomeView.as_view(), name='home')

]
