from django_filters import AllValuesMultipleFilter, rest_framework, widgets
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = rest_framework.BooleanFilter(widget=widgets.BooleanWidget())
    is_in_shopping_cart = rest_framework.BooleanFilter(
        widget=widgets.BooleanWidget()
    )

    class Meta:
        model = Recipe
        fields = ['tags__slug']


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
