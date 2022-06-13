from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
    path('signin/', auth_views.LoginView.as_view(template_name='api/index.html')),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_user, name='activate'),
    path('home/', views.home, name="home"),
    path('upload_pfp/', views.upload_pfp, name="upload_pfp"),
    path('profile/', views.profile, name="profile"),
    path('display_own_grades/', views.display_own_grades, name="display_own_grades"),
    path('individual_evaluation_report/', views.individual_evaluation_report, name="individual_evaluation_report"),
    path('faculty_evaluation/', views.faculty_evaluation, name="faculty_evaluation"),
    path('ledger_of_accounts/', views.ledger_of_accounts, name="ledger_of_accounts"),
    path('transactions/', views.transactions, name="transactions"),
    path('apply_for_graduation/', views.apply_for_graduation, name="apply_for_graduation"),
]