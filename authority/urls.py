from django.urls import path
from authority.views import (
    add_permission,
    delete_permission,
    approve_permission_request,
    delete_permission,
)


urlpatterns = [
    path(
        "permission/add/<app_label>/<module_name>/<int:pk>/",
        view=add_permission,
        name="authority-add-permission",
        kwargs={"approved": True},
    ),
    path(
        "permission/delete/<int:permission_pk>/",
        view=delete_permission,
        name="authority-delete-permission",
        kwargs={"approved": True},
    ),
    path(
        "request/add/<app_label>/<module_name>/<int:pk>/",
        view=add_permission,
        name="authority-add-permission-request",
        kwargs={"approved": False},
    ),
    path(
        "request/approve/<int:permission_pk>/",
        view=approve_permission_request,
        name="authority-approve-permission-request",
    ),
    path(
        "request/delete/<int:permission_pk>/",
        view=delete_permission,
        name="authority-delete-permission-request",
        kwargs={"approved": False},
    ),
]
