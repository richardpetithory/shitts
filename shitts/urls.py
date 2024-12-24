from django.contrib import admin
from django.urls import path

from api import views as api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", shop_views.rent_due),
    path("graphql/", api_views.graphql_view, name="graphql"),
]
