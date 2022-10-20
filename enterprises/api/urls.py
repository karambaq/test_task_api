from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    OrganizationViewSet,
    DistrictViewSet,
    CategoryViewSet,
    get_orgs_by_district,
    OrgProductViewSet,
)

app_name = "api"
router = DefaultRouter()

router.register("products", ProductViewSet, basename="products")
router.register("districts", DistrictViewSet, basename="districts")
router.register("categories", CategoryViewSet, basename="categories")
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("org_products", OrgProductViewSet, basename="org_products")
router.register(
    "organizations/(?P<district_id>\d+)",
    OrganizationViewSet,
    basename="organizations_by_district",
)
router.register(
    "organizations/detail/(?P<organization_id>\d+)",
    OrganizationViewSet,
    basename="organizations_detail",
)

urlpatterns = [
    path(
        "organizations/<int:district_id>/",
        get_orgs_by_district,
        name="org_by_district",
    ),
    path("", include(router.urls), name="api"),
]
