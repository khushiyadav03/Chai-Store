from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_chai, name="menu"),
    path("<int:chai_id>/", views.chai_detail, name="chai_detail"),
    path("stores/", views.chai_store_view, name="chai_stores"),
]
