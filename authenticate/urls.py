from django.urls import path
from authenticate.views import *

app_name = "auth"

urlpatterns = [
    # First Landing Page
    path("", first_auth_page, name="first_auth_page"),
    
    # Login
    path("login/", login, name="login"),
    
    # Logout
    path("logout/", logout, name="logout"),
    
    # Register
    path("register/pelanggan/", register_pelanggan, name="register_pelanggan"),
    path("register/pekerja/", register_pekerja, name="register_pekerja"),
    path("register/", register, name="register"),
    
    # Profile
    path("profile/", profile, name="profile"),
    path("profile/edit/", updateProfile, name="edit_profile"),
    path("profile/<id>/", worker_profile, name="worker_profile"),
]
