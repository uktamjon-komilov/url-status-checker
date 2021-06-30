from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_of_urls, name = "list_of_urls"),
    path("create/", views.add_url, name = "add_url"),
    path("update/<int:_id>", views.update_url, name = "update_url")
]