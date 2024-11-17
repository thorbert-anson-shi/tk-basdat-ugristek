from django.urls import path
from authenticate.views import *

urlpatterns = [
    path("", begin, name="begin"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/pengguna/", register_pengguna, name="register_pengguna"),
    path("register/pekerja/", register_pekerja, name="register_pekerja"),
    path("register/", register, name="register"),
    path("navbar/", navbar, name="navbar"),
     path('profile/', profile, name='profile'),
]
