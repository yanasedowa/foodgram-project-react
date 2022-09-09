def get_cart(ingredients):
    cart = '\n'.join([
        f'{ingredient["ingredients__name"]} - {ingredient["total"]} '
        f'{ingredient["ingredients__measurement_unit"]}'
        for ingredient in ingredients
    ])
    return cart
