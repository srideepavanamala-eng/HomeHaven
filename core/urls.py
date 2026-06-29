from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),

    path("register/", views.register_view, name="register"),

    path("owner/", views.owner_dashboard, name="owner_dashboard"),

    path("tenant/", views.tenant_dashboard, name="tenant_dashboard"),

    path("add-property/", views.add_property, name="add_property"),
     
    path(
      "edit-property/<int:property_id>/",
      views.edit_property,
      name="edit_property"
    ),
    path(
    "delete-property/<int:property_id>/",
    views.delete_property,
    name="delete_property"
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
    "property/<int:property_id>/",
    views.property_details,
    name="property_details"
),
path(
    "contact-owner/<int:property_id>/",
    views.contact_owner,
    name="contact_owner"
),
path(
    "interested-tenants/",
    views.interested_tenants,
    name="interested_tenants"
),
]