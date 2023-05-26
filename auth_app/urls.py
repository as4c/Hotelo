from django.urls import path
from . import views

# app_name='account'
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.user_login,name='signin'),
    path('signout/',views.user_logout,name='signout'),
    path('profile/',views.profile,name="profile"),
]

