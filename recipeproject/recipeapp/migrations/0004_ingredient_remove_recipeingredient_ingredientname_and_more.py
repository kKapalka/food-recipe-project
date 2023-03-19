# Generated by Django 4.1.7 on 2023-03-17 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0003_recipeingredient_recipeid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ingredientName', models.TextField()),
            ],
            options={
                'db_table': 'ingredient',
            },
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='ingredientName',
        ),
        migrations.RemoveField(
            model_name='recipeingredientfood',
            name='recipeIngredientId',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredientId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipeapp.ingredient'),
        ),
        migrations.AddField(
            model_name='recipeingredientfood',
            name='ingredientId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipeapp.ingredient'),
        ),
    ]
