import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.BooleanFilter()
    is_in_shopping_cart = django_filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ['tags__slug']


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
