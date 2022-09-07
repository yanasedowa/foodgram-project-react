# Generated by Django 3.2 on 2022-09-07 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220906_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['-id'], 'verbose_name': 'Список покупок'},
        ),
        migrations.RemoveConstraint(
            model_name='shoppingcart',
            name='unique_cart_user',
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_cart'),
        ),
    ]
