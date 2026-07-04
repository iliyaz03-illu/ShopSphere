from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Shoes", "Shoes"),
        ("Watches", "Watches"),
    ]

    name = models.CharField(max_length=200)

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/"
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name