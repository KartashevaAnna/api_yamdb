from api.views import (
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewViewSet
)
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/v1/categories", CategoriesViewSet)
router.register(r"api/v1/genres", GenresViewSet)
router.register(r"api/v1/titles", TitlesViewSet)
router.register(r"api/v1/reviews", ReviewViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("redoc/", TemplateView.as_view(template_name="redoc.html"), name="redoc"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("", include(router.urls)),
]
