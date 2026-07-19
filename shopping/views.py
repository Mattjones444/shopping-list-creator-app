from django.views.generic import DetailView, ListView

from .models import Meal


class MealListView(ListView):
    model = Meal
    template_name = "shopping/meal_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        return Meal.objects.filter(active=True)


class MealDetailView(DetailView):
    model = Meal
    template_name = "shopping/meal_detail.html"
    context_object_name = "meal"

    def get_queryset(self):
        return (
            Meal.objects
            .filter(active=True)
            .prefetch_related("meal_products__product")
        )

