from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/categories', CategoriesViewSet)
router.register(r'api/v1/genres', GenresViewSet)
router.register(r'api/v1/titles', TitlesViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
