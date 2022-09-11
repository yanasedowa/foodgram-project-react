import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.BooleanFilter()
    is_in_shopping_cart = django_filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ['tags__slug']


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
