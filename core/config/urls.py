from django.contrib import admin
from django.urls import include, path
# from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework import routers
from API.views import OfferApiViewSet

router = routers.DefaultRouter()

router.register('', OfferApiViewSet, basename='offer-list')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    # path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
