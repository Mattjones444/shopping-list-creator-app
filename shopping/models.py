from django.db import models

from django.core.validators import MinValueValidator
from django.db import models


class ShoppingSection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    class Unit(models.TextChoices):
        GRAM = "g", "Grams"
        KILOGRAM = "kg", "Kilograms"
        MILLILITRE = "ml", "Millilitres"
        LITRE = "l", "Litres"
        ITEM = "item", "Item"
        PACK = "pack", "Pack"
        TIN = "tin", "Tin"
        BOTTLE = "bottle", "Bottle"
        TABLESPOON = "tbsp", "Tablespoon"
        TEASPOON = "tsp", "Teaspoon"

    name = models.CharField(max_length=150, unique=True)

    shopping_section = models.ForeignKey(
        ShoppingSection,
        on_delete=models.PROTECT,
        related_name="products",
    )

    default_unit = models.CharField(
        max_length=20,
        choices=Unit.choices,
        default=Unit.ITEM,
    )

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=150, unique=True)

    description = models.TextField(blank=True)

    instructions = models.TextField(blank=True)

    base_servings = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1)],
    )

    image = models.ImageField(
        upload_to="meal_images/",
        blank=True,
        null=True,
    )

    favourite = models.BooleanField(default=False)

    active = models.BooleanField(default=True)

    products = models.ManyToManyField(
        Product,
        through="MealProduct",
        related_name="meals",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MealProduct(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name="meal_products",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="meal_products",
    )

    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    unit = models.CharField(
        max_length=20,
        choices=Product.Unit.choices,
    )

    notes = models.CharField(
        max_length=200,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["meal", "product"],
                name="unique_product_per_meal",
            )
        ]
        ordering = ["product__name"]

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.product} for {self.meal}"
