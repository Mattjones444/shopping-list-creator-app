from django.urls import path

from .views import MealDetailView, MealListView

app_name = "shopping"

urlpatterns = [
    path("", MealListView.as_view(), name="meal-list"),
    path("meals/<int:pk>/", MealDetailView.as_view(), name="meal-detail"),
]