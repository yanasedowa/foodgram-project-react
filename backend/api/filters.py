from django.contrib.auth import get_user_model
from django_filters import FilterSet, ModelMultipleChoiceFilter, rest_framework
from django_filters.widgets import BooleanWidget
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = rest_framework.BooleanFilter(widget=BooleanWidget())
    is_in_shopping_cart = rest_framework.BooleanFilter(widget=BooleanWidget())
    author = ModelMultipleChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = [
            'tags__slug',
            'author__id',
        ]


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
