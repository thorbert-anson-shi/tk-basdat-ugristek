from django.urls import path
from . import views

urlpatterns = [
    path('', views.subkategori_list, name='subkategori_list'),
    path('<uuid:id>/', views.subkategori_detail, name='subkategori_detail'),
]