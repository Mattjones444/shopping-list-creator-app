from django.contrib import admin

from .models import Meal, MealProduct, Product, ShoppingSection


class MealProductInline(admin.TabularInline):
    model = MealProduct
    extra = 1


@admin.register(ShoppingSection)
class ShoppingSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    ordering = ("display_order", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shopping_section", "default_unit", "active")
    list_filter = ("shopping_section", "default_unit", "active")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "base_servings", "favourite", "active", "updated_at")
    list_filter = ("favourite", "active")
    search_fields = ("name", "description")
    ordering = ("name",)
    inlines = [MealProductInline]


@admin.register(MealProduct)
class MealProductAdmin(admin.ModelAdmin):
    list_display = ("meal", "product", "quantity", "unit")
    list_filter = ("unit",)
    search_fields = ("meal__name", "product__name")