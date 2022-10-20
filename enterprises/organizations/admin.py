from django.contrib import admin

from .models import (
    District,
    Category,
    OrganizationNetwork,
    Organization,
    OrganizationProduct,
    Product,
)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationNetwork)
class OrganizationNetworkAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationProduct)
class OrganizationProductAdmin(admin.ModelAdmin):
    pass
