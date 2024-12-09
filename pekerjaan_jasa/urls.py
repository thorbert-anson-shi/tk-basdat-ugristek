from django.urls import path
from pekerjaan_jasa.views import *

app_name = "pekerjaan_jasa"

urlpatterns = [
    path("", home, name="home"),
    path("list", pekerjaan_list, name="pekerjaan_list"),
    path("get_subkategori/", get_subcategories, name="get_subcategories"),
    path("get_kategori/", get_categories, name="get_categories"),
    path("get_tickets/", get_tickets, name="get_tickets"),
    path("get_status_choices/", get_status_choices, name="get_status_choices"),
    path("update_ticket_status/", update_ticket_status, name="update_ticket_status"),
    path("take_ticket/", take_ticket, name="take_ticket"),
]
