from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_of_urls, "list_of_urls"),
    path("create/", views.add_url, "add_url"),
    path("update/", views.update_url, "update_url")
]