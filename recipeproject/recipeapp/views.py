import json

from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Ingredient, NewIngredient, IngredientSynonym
from fuzzywuzzy import fuzz
import spacy

nlp = spacy.load('en_core_web_sm')

@require_GET
def search_ingredients(request):
    query = request.GET.get('query', '')

    # search for matching ingredients using the 'icontains' lookup
    synonym_ingredient_ids = IngredientSynonym.objects.values_list('ingredient_id', flat=True)
    matching_ingredients = Ingredient.objects.filter(name__icontains=query).exclude(id__in=synonym_ingredient_ids)[:50]

    # convert the matching ingredients queryset to a list of dictionaries
    results = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in matching_ingredients]

    # return the results as a JSON response
    return JsonResponse({'results': results})


@require_GET
def search_related_ingredients_1(request):
    new_ingredient_id = request.GET.get('newIngredientId')
    if not new_ingredient_id:
        return JsonResponse({'error': 'newIngredientId parameter is missing'}, status=400)
    new_ingredient = NewIngredient.objects.get(id=new_ingredient_id)
    synonym_ingredients = IngredientSynonym.objects.filter(new_ingredient_id=new_ingredient_id).values_list(
        'ingredient_id', flat=True)
    ingredient_names = set(Ingredient.objects.exclude(id__in=synonym_ingredients).values_list('name', flat=True))
    similarity_scores = {}
    for name in ingredient_names:
        similarity_scores[name] = nlp(new_ingredient.name).similarity(nlp(name))
    sorted_ingredients = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    related_ingredients = [Ingredient.objects.get(name=name) for name, score in sorted_ingredients][:50]
    response_data = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in related_ingredients]
    return JsonResponse({'results': response_data})


@require_GET
def search_related_ingredients(request):
    new_ingredient_id = request.GET.get('newIngredientId')
    if not new_ingredient_id:
        return JsonResponse({'error': 'newIngredientId parameter is missing'}, status=400)
    related_ingredients = IngredientSynonym.objects.values_list(
        'ingredient_id', flat=True)
    available_ingredients = Ingredient.objects.exclude(Q(pk__in=related_ingredients))
    related_ingredient_names = IngredientSynonym.objects.filter(new_ingredient_id=new_ingredient_id).values_list(
        'ingredient__name', flat=True)
    related_ingredient_names = set(name.lower() for name in related_ingredient_names)
    sorted_ingredients = sorted(available_ingredients, key=lambda ingredient: max(
        [fuzz.token_set_ratio(name.lower(), ingredient.name.lower()) for name in related_ingredient_names]),
                                reverse=True)[:200]
    response_data = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in sorted_ingredients]
    return JsonResponse({'results': response_data})


def getFirstPassSortedIngredients(new_ingredient_id):
    related_ingredients = IngredientSynonym.objects.values_list(
    'ingredient_id', flat=True)

    # Get all ingredients not present in the ingredient_synonym table
    available_ingredients = Ingredient.objects.exclude(Q(pk__in=related_ingredients) | Q(pk=new_ingredient_id))

    # Sort available ingredients by their similarity to all the ingredient names occurring in the synonym table
    related_ingredient_names = IngredientSynonym.objects.filter(new_ingredient_id=new_ingredient_id).values_list(
        'ingredient__name', flat=True)
    related_ingredient_names = set(name.lower() for name in related_ingredient_names)
    sorted_ingredients = sorted(available_ingredients, key=lambda ingredient: max(
        [fuzz.token_set_ratio(name.lower(), ingredient.name.lower()) for name in related_ingredient_names]),
                                reverse=True)[:1000]
    return sorted_ingredients



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
