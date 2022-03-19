from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)

    price = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ])

    image = models.ImageField(blank=True, upload_to="...images")

    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    categories = models.ManyToManyField(
        Category,
        related_name='product_categories',
        through='ProductCategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"


class ProductCategories(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        db_table = 'product_categories'
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'category'),
                name='unique_product_category'
            )
        ]