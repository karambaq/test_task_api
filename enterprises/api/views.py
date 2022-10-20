from rest_framework import filters, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from organizations.models import (
    Product,
    Organization,
    District,
    Category,
    OrganizationProduct,
)
from .serializers import (
    ProductReadSerializer,
    ProductCreateSerializer,
    OrganizationSerializer,
    OrgProductSerializer,
    DistrictSerializer,
    CategorySerializer,
)
from .mixins import ListRetrieveViewSet


class ProductViewSet(mixins.CreateModelMixin, ListRetrieveViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductReadSerializer


class DistrictViewSet(ListRetrieveViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class CategoryViewSet(ListRetrieveViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class OrgProductViewSet(ListRetrieveViewSet):
    serializer_class = OrgProductSerializer
    queryset = OrganizationProduct.objects.all()


class OrganizationViewSet(ListRetrieveViewSet):
    serializer_class = OrganizationSerializer
    filterset_fields = ("products__category",)
    ordering_fields = ("org_products__price",)
    search_fields = (
        "id",
        "description",
        "name",
        "org_products__product__name",
    )
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    def get_queryset(self):
        org_id = self.kwargs.get("organization_id")
        if org_id:
            return Organization.objects.filter(id=org_id)
        return Organization.objects.all()


@api_view(http_method_names=["GET"])
def get_orgs_by_district(request, district_id):
    objs = Organization.objects.filter(districts__in=[district_id])
    data = OrganizationSerializer(objs, many=True).data
    return Response(data, status=200)
