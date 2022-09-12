from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FollowViewSet, IngredientsViewSet, RecipeViewSet,
                       TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipeViewSet)
#router.register('users', FollowViewSet)
router.register(
    r'users/(?P<following_id>\d+)/subscribe', FollowViewSet.as_view()
)
#router.register(
#     r'recipes/download_shopping_cart', ShoppingCartViewSet
# )
# router.register(
#     r'recipes/(?P<recipes_id>\d+)/shopping_cart', ShoppingCartViewSet
# )
# router.register(
#     r'recipes/(?P<recipes_id>\d+)/favorite', FavoriteViewSet
# )

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
