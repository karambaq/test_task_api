from rest_framework import serializers

from organizations.models import (
    Product,
    Organization,
    District,
    Category,
    OrganizationProduct,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = (fields,)


class OrgProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProduct
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    products = OrgProductSerializer(source="org_products", many=True)

    class Meta:
        model = Organization
        fields = "__all__"
