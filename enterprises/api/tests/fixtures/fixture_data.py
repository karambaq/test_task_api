import pytest


@pytest.fixture
def district_fix():
    from organizations.models import District

    district = District.objects.create(
        name="Test_District",
    )
    return district


@pytest.fixture
def org():
    from organizations.models import (
        Organization,
        District,
        Product,
        Category,
        OrganizationProduct,
    )

    district = District.objects.create(
        name="District",
    )

    category = Category.objects.create(name="TestCategory")
    product = Product.objects.create(name="TestProduct", category=category)

    another_district = District.objects.create(
        name="Another_District",
    )

    org = Organization.objects.create(
        name="Organization", description="Description"
    )
    org.districts.add(district)
    another_org = Organization.objects.create(
        name="AnotherOrganization", description="AnotherDescription"
    )
    OrganizationProduct.objects.create(
        price=10, organization=another_org, product=product
    )
    OrganizationProduct.objects.create(
        price=1, organization=org, product=product
    )
    another_org.districts.add(another_district)
    return another_org
