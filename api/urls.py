from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('signout/', views.signout, name="signout"),
    path('signin/', auth_views.LoginView.as_view(template_name='api/index.html')),
]