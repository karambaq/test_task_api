from django.db import models


class District(models.Model):
    name = models.CharField("Название района", max_length=100, unique=True)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        app_label = "organizations"

    def __str__(self):
        return f"Район: {self.name}"


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        app_label = "organizations"

    def __str__(self):
        return f"Категория {self.name}"


class OrganizationNetwork(models.Model):
    name = models.CharField(
        "Название сети предприятий", max_length=100, unique=True
    )
    # У одной сети предприятий могут быть одинаковые категории.
    categories = models.ManyToManyField(
        "Category",
        related_name="org_networks",
    )

    class Meta:
        verbose_name = "Сеть организаций"
        verbose_name_plural = "Сети организаций"
        app_label = "organizations"

    def __str__(self):
        return f"Сеть организаций {self.name}"


class Organization(models.Model):
    name = models.CharField(
        "Название предприятия", max_length=100, unique=True
    )
    description = models.TextField("Описание предприятия")
    organization_network = models.ForeignKey(
        OrganizationNetwork,
        on_delete=models.CASCADE,
        related_name="organizations",
        blank=True,
        null=True,
    )
    districts = models.ManyToManyField(
        "District",
        related_name="organizations",
        blank=True,
    )
    products = models.ManyToManyField(
        "Product",
        through="OrganizationProduct",
        through_fields=("organization", "product"),
        related_name="organizations",
    )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        app_label = "organizations"

    def __str__(self):
        return f"Организация {self.name}, {self.description}"


class Product(models.Model):
    name = models.CharField("Название товара/услуги", max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    class Meta:
        verbose_name = "Товар/Услуга"
        verbose_name_plural = "Товары/Услуги"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "category"), name="Unique name for category"
            )
        ]
        app_label = "organizations"

    def __str__(self):
        return f"Товар/услуга: {self.name}"


class OrganizationProduct(models.Model):
    """
    Так как цена может зависеть от предприятия, делаем отдельную таблицу с дополнительным полем.
    """

    price = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="org_products"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="org_products"
    )

    class Meta:
        verbose_name = "Товары организации"
        verbose_name_plural = "Товары организаций"
        app_label = "organizations"
        constraints = [
            models.UniqueConstraint(
                fields=("product", "organization"),
                name="Unique product for organization",
            )
        ]

    def __str__(self):
        return f"Услуга/товар организации: {self.price}, {self.organization}, {self.product}"


# class DistrictOrganization(models.Model):
#     district = models.ForeignKey(
#         District, on_delete=models.CASCADE, related_name="district_orgs"
#     )
#     organization = models.ForeignKey(
#         Organization, on_delete=models.CASCADE, related_name="district_orgs"
#     )

#     class Meta:
#         verbose_name = "Районы организации"
#         verbose_name_plural = "Районы организаций"
#         app_label = "organizations"

#     def __str__(self):
#         return f"Район организации: {self.district}, {self.organization}"


# class OrganizationNetworkCategory(models.Model):
#     org_network = models.ForeignKey(
#         OrganizationNetwork,
#         on_delete=models.CASCADE,
#         related_name="orgs_network_categories",
#     )
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name="orgs_network_categories",
#     )
#
#     class Meta:
#         verbose_name = "Категории сети организаций"
#         verbose_name_plural = "Категории сетей организаций"
#         app_label = "organizations"
#
#     def __str__(self):
#         return f"Категории организации: {self.org_network}, {self.category}"
