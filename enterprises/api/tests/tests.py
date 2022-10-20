import pytest
from django.urls import reverse

from organizations.models import (
    Organization,
    Category,
    District,
    Product,
)


class TestPostAPI:
    def _check_json_ids(self, response, expected_ids, error_message):
        json_data = response.json()
        received_orgs = []
        for val in json_data:
            received_orgs.append(val.get("id"))
        assert received_orgs == expected_ids, error_message

    @pytest.mark.django_db(transaction=True)
    def test_token_needed(self, client):
        url = reverse("api:organizations-list")
        response = client.get(url)
        assert (
            response.status_code == 401
        ), "Проверьте, что API защищён токеном"

    # 1) Список заведений - с условием заранее выбранного района:
    # • url: /organizations/<district_id>/
    @pytest.mark.django_db(transaction=True)
    def test_orgs_filtered_by_district(self, user_client, org):
        district = District.objects.last()
        expected_orgs = list(
            Organization.objects.filter(districts__in=[district]).values_list(
                "id", flat=True
            )
        )
        url = reverse(
            "api:org_by_district", kwargs={"district_id": district.id}
        )
        response = user_client.get(url)
        self._check_json_ids(
            response,
            expected_orgs,
            "Проверьте, что фильтрация по району работает верно",
        )

    # # • фильтры: по цене (максимальная\минимальная)
    @pytest.mark.django_db(transaction=True)
    def test_org_can_be_filtered_by_price_desc(self, user_client, org):
        expected_ids_order = list(
            Organization.objects.order_by("-org_products__price").values_list(
                "id", flat=True
            )
        )
        url = (
            reverse("api:organizations-list")
            + "?ordering=-org_products__price"
        )
        response = user_client.get(url)
        self._check_json_ids(
            response,
            expected_ids_order,
            "Проверьте, что сортировка по убыванию работает верно",
        )

    @pytest.mark.django_db(transaction=True)
    def test_org_can_be_filtered_by_price_asc(self, user_client):
        expected_ids_order = list(
            Organization.objects.order_by("org_products__price").values_list(
                "id", flat=True
            )
        )
        url = (
            reverse("api:organizations-list") + "?ordering=org_products__price"
        )
        response = user_client.get(url)
        self._check_json_ids(
            response,
            expected_ids_order,
            "Проверьте, что сортировка по возрастанию работает верно",
        )

    # по категории товаров\услуг в этом заведении
    @pytest.mark.django_db(transaction=True)
    def test_org_can_be_filtered_by_category(self, user_client, org):
        category = Category.objects.last().id
        expected_ids_order = list(
            Organization.objects.filter(
                products__category=category
            ).values_list("id", flat=True)
        )
        url = (
            reverse("api:organizations-list")
            + f"?products__category={category}"
        )
        response = user_client.get(url)
        self._check_json_ids(
            response,
            expected_ids_order,
            "Проверьте, что работает фильтрация организация по категории",
        )

    #  поиск по названию товара\услуги
    @pytest.mark.django_db(transaction=True)
    def test_org_can_be_searched_by_name(self, user_client, org):
        product = Product.objects.last()
        expected_ids_order = list(
            Organization.objects.filter(
                products__name=product.name
            ).values_list("id", flat=True)
        )
        url = reverse("api:organizations-list") + f"?search={product.name}"
        response = user_client.get(url)
        self._check_json_ids(
            response,
            expected_ids_order,
            "Проверьте, что работает поиск организаций по названию товара",
        )

    #
    # 2) Детальная информация по заведению
    @pytest.mark.django_db(transaction=True)
    def test_detail_org_view(self, user_client, org):
        organization = Organization.objects.last()
        url = reverse(
            "api:organizations_detail-list",
            kwargs={"organization_id": organization.id},
        )
        response = user_client.get(url)
        json_data = response.json()[0]
        org_id = json_data.get("id")
        org_name = json_data.get("name")
        org_desc = json_data.get("description")
        assert organization.id == org_id, "У объектов не совпадают id"
        assert organization.name == org_name, "У объектов не совпадают имена"
        assert (
            organization.description == org_desc
        ), "У объектов не совпадают описания"

    #
    # # 3) Добавление товара/услуги
    @pytest.mark.django_db(transaction=True)
    def test_product_create(self, user_client, org):
        category = Category.objects.last()
        url = reverse("api:products-list")
        data = {"name": "TestProduct1", "category": category.id}
        response = user_client.post(
            url, data={"name": "TestProduct1", "category": category.id}
        )
        json_data = response.json()
        assert (
            response.status_code == 201
        ), "Сервер вернул отличный от 200 код ответа"
        created_product = Product.objects.last()
        assert created_product.id == json_data.get(
            "id"
        ), "У объектов не совпадают id"
        assert created_product.name == data.get(
            "name"
        ), "У объектов не совпадают name"
        assert created_product.category.id == data.get(
            "category"
        ), "У объектов не совпадают category"

    # 4) Детальная информация по товару\услуге
    @pytest.mark.django_db(transaction=True)
    def test_product_detail_view(self, user_client, org):
        last_product = Product.objects.last()
        url = reverse("api:products-detail", kwargs={"pk": last_product.id})
        response = user_client.get(url)
        json_data = response.json()
        assert last_product.id == json_data.get("id")
        assert last_product.name == json_data.get("name")
        assert last_product.category.id == json_data.get("category").get("id")
