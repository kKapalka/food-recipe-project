import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Ingredient, NewIngredient, IngredientSynonym
from fuzzywuzzy import fuzz


@csrf_exempt
@require_POST
def search_ingredients_with_synonyms(request):

    data = json.loads(request.body)
    keyword = data.get('keyword', '')
    new_ingredient_id = data.get('newIngredientId', '')

    synonym_ingredient_ids = IngredientSynonym.objects.values_list('ingredient_id', flat=True)
    available_ingredients = Ingredient.objects.exclude(id__in=synonym_ingredient_ids)
    # Filter by keyword
    if keyword:
        available_ingredients = available_ingredients.filter(name__icontains=keyword)

    # Exclude existing ingredients and synonyms
    if new_ingredient_id:
        related_ingredients = IngredientSynonym.objects.filter(new_ingredient_id=new_ingredient_id).values_list(
            'ingredient_id', flat=True)
        available_ingredients = available_ingredients.exclude(
            Q(pk__in=related_ingredients) | Q(pk=new_ingredient_id))

    # Sort by similarity to existing synonyms
    if new_ingredient_id:
        related_ingredient_names = IngredientSynonym.objects.filter(new_ingredient_id=new_ingredient_id).values_list(
            'ingredient__name', flat=True)
        related_ingredient_names = set(name.lower() for name in related_ingredient_names)
        sorted_ingredients = sorted(available_ingredients, key=lambda ingredient: max(
            [fuzz.token_set_ratio(name.lower(), ingredient.name.lower()) for name in related_ingredient_names]),
                                    reverse=True)
    else:
        sorted_ingredients = sorted(available_ingredients, key=lambda ingredient: fuzz.token_set_ratio(keyword.lower(), ingredient.name.lower()),
                                    reverse=True)

    response_data = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in sorted_ingredients]
    return JsonResponse({'results': response_data})



@csrf_exempt
@require_POST
def create_new_ingredient(request):
    data = json.loads(request.body)
    name = data.get('name', '')
    if name:
        new_ingredient = NewIngredient.objects.create(name=name)
        return JsonResponse({'id': new_ingredient.id, 'name': new_ingredient.name})

@csrf_exempt
@require_POST
def create_ingredient_synonym(request):
    data = json.loads(request.body)
    ingredient_id = data.get('ingredientId', '')
    new_ingredient_id = data.get('newIngredientId', '')
    ingredient = Ingredient.objects.get(id=ingredient_id)
    new_ingredient = NewIngredient.objects.get(id=new_ingredient_id)
    synonym = IngredientSynonym.objects.create(ingredient=ingredient, new_ingredient=new_ingredient)
    return JsonResponse({'id': synonym.id})

@require_GET
def search_new_ingredients(request):

    # search for matching ingredients using the 'icontains' lookup
    newIngredients = NewIngredient.objects.all()

    # convert the matching ingredients queryset to a list of dictionaries
    results = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in newIngredients]

    # return the results as a JSON response
    return JsonResponse({'results': results})
