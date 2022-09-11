from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientAddToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    ingredient = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = IngredientAmount
        fields = ['id', 'ingredient', 'amount']


class RecipePreviewSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким email уже зарегистрирован')
        ]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким именем уже зарегистрирован')
        ]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipePreviewSerializer(queryset, many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredient_amount'
    )
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name', 'image',
                  'text', 'cooking_time',)

    # def get_is_favorited(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     if Favorite.objects.filter(user=request.user,
    #                                recipe__id=obj.id).exists():
    #         return True
    #     return False

    # def get_is_in_shopping_cart(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     if ShoppingCart.objects.filter(
    #         user=request.user,
    #         recipe__id=obj.id
    #     ).exists():
    #         return True
    #     return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAddToRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredients_validated = []
        for ingredient in ingredients:
            if type(ingredient.get('amount')) is not int:
                raise serializers.ValidationError(
                    ('Неверный формат данных.')
                )
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    ('Минимальное количество ингредиентов 1.')
                )
            if data.get('cooking_time') <= 0:
                raise serializers.ValidationError(
                    'Минимальное время 1 минута.'
                )
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_validated:
                raise serializers.ValidationError(
                    'Ингредиент уже добавлен.'
                )
            ingredients_validated.append(ingredient_id)
        data['ingredients'] = ingredients
        return data

    def add_ingredient_tags(self, instance, **validated_data):
        ingredients = validated_data['ingredients']
        tags = validated_data['tags']
        for tag in tags:
            instance.tags.add(tag)
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['id'],
            recipe=instance,
            amount=ingredient['amount']
        ) for ingredient in ingredients])
        return instance

    def create(self, validated_data):
        tags = self.initial_data.get('tags')
        ingredients = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(
            image=image,
            **validated_data,
            author=self.context.get('request').user
        )
        return self.add_ingredient_tags(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.create_ingredient(ingredients, instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = '__all__'
