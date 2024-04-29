from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    # path('roadmap/', views.RoadmapPage, name='roadmap'),
    # path('about/', views.AboutPage, name='about'),
    # path('login/', views.LoginPage, name='login'),
    # path('signup/', views.SignupPage, name='signup'),
    # path('logout/',views.LogoutPage, name='logout'),
    # path('profile/',views.ProfilePage, name='profile'),
]
