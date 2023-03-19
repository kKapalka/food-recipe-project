# Generated by Django 4.1.7 on 2023-03-17 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ingredientName', models.TextField()),
            ],
            options={
                'db_table': 'recipe_ingredient',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientFood',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('foodId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='recipeapp.food')),
                ('recipeIngredientId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='recipeapp.recipeingredient')),
            ],
            options={
                'db_table': 'recipe_ingredient_food',
            },
        ),
    ]
