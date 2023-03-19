"""recipeproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from recipeapp.views import search_ingredients, create_new_ingredient, search_new_ingredients, \
    create_ingredient_synonym, search_related_ingredients

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ingredients/search', search_ingredients, name='search_ingredients'),
    path('new-ingredient/', create_new_ingredient, name='create_new_ingredient'),
    path('new-ingredients/search', search_new_ingredients, name='search_new_ingredients'),
    path('synonym/', create_ingredient_synonym, name='create_ingredient_synonym'),
    path('related-ingredients/search', search_related_ingredients, name='search_related_ingredients'),

]
