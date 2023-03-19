# Generated by Django 4.1.7 on 2023-03-18 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0005_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientSynonym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'ingredient_synonym',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NewIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'new_ingredient',
                'managed': False,
            },
        ),
    ]
