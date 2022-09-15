from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Exists, OuterRef, Sum, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AdminOrReadOnly, AdminUserOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipePreviewSerializer, RecipeSerializer,
                          TagSerializer)
from .utils import get_cart

User = get_user_model()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AdminUserOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                )
            )
        else:
            queryset = queryset.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return queryset

    @action(
        methods=['post'],
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        if ShoppingCart.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                'Рецепт уже есть в списке',
                status=HTTPStatus.BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = RecipePreviewSerializer(recipe)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @shopping_cart.mapping.delete
    def delele_from_shopping_cart(self, request, pk=None):
        user = request.user
        cart = ShoppingCart.objects.filter(user=user, recipe__id=pk)
        if cart.exists():
            cart.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            'Невозможно удалить рецепт из списка',
            status=HTTPStatus.BAD_REQUEST
        )

    @action(
        methods=['get'],
        detail=False
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredients__name',
            'ingredients__measurement_unit').annotate(total=Sum('amount'))
        shopping_cart = get_cart(ingredients)
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        methods=['post'],
        detail=True,
    )
    def favorite(self, request, pk=None):
        user = request.user
        if Favorite.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                'Рецепт уже в Избранном',
                status=HTTPStatus.BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer()
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @favorite.mapping.delete
    def delele_from_favorite(self, request, pk=None):
        user = request.user
        favorite = Favorite.objects.filter(user=user, recipe__id=pk)
        if favorite.exists():
            favorite.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            'Невозможно удалить рецепт из Избранного',
            status=HTTPStatus.BAD_REQUEST
        )


class FollowViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                'Нельзя подписаться на себя',
                status=HTTPStatus.BAD_REQUEST
            )
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                'Такая подписка уже существует',
                status=HTTPStatus.BAD_REQUEST
            )
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(follow, context={'request': request})
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                'Нельзя отписаться от самого себя',
                status=HTTPStatus.BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if not follow.exists():
            return Response(
                'Вы не подписаны',
                status=HTTPStatus.BAD_REQUEST)
        follow.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
