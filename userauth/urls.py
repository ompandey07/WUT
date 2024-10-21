from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view , name="login_view"),
    path('register/', views.register_view, name='register'),
    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),
    path('logout/', views.logout_view, name="logout_view"),
    path('profile/', views.user_profile_view, name='user_profile'),



    path('work/', views.work_view, name='work'),
    
]