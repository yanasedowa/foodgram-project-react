from django.contrib.auth import get_user_model
import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = django_filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_shopping_cart'
    )
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all()
    )

    def filter_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'tags__slug',
            'author__id',
            'is_favorited',
            'is_in_shopping_cart'
        ]


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
