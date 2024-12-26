from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from api import views as api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", serve, {"path": "index.html", "document_root": settings.STATIC_ROOT}),
    path("graphql/", api_views.graphql_view, name="graphql"),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(
        r"^assets/(?P<path>.*)$",
        serve,
        {"document_root": settings.STATIC_ROOT + "/assets"},
    ),
]
