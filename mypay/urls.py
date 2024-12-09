from django.urls import path
from .views import *

app_name = "mypay"

urlpatterns = [
    path("", home, name="home"),
    path("fetch_transactions/", fetch_transactions, name="fetch_transactions"),
    path("fetch_bills/", fetch_bills, name="fetch_bills"),
    path("fetch_banks/", fetch_banks, name="fetch_banks"),
    path("topup/", handle_topup, name="handle_topup"),
    path("withdrawal/", handle_withdrawal, name="handle_withdrawal"),
    path("transfer/", handle_transfer, name="handle_transfer"),
    path("payment/", handle_payment, name="handle_payment"),
]
