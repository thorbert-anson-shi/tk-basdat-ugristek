from django.urls import path
from .views import home

app_name = "mypay"

urlpatterns = [path("", home, name="home")]
