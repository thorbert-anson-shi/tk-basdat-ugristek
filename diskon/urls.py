from django.urls import path
from diskon.views import show_hal_diskon

app_name = 'main'

urlpatterns = [
    path('', show_hal_diskon, name='show_hal_diskon'),
]