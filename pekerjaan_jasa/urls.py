from django.urls import path
from pekerjaan_jasa.views import *

urlpatterns = [
    path("", home, name="home"),
    path("list", pekerjaan_list, name="pekerjaan_list"),
    path("get_subkategori/", get_subcategories, name="get_subcategories"),
    path("get_kategori/", get_categories, name="get_categories"),
    path("get_tickets/", get_tickets, name="get_tickets"),
]
