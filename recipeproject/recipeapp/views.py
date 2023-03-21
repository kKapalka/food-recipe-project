import json
from collections import Counter

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Ingredient, NewIngredient, IngredientSynonym

import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
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
def search_clustered_ingredients(request):
    data = json.loads(request.body)
    name = data.get('name', '')
    eps = data.get('epsilon', '')
    min_samples = data.get('min_samples', '')
    available_ingredients = Ingredient.objects.filter(name__icontains=name)

    # Convert the text to a matrix of TF-IDF features
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([ingredient.name + ' ' + name + ' ' + name for ingredient in available_ingredients])

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(X)
    labels = dbscan.labels_
    clusteredCount = 0
    clustered_ingredients = []

    for i in range(max(labels) + 1):
        ingredient_cluster = []
        for j in range(len(available_ingredients)):
            if labels[j] == i:
                ingredient_cluster.append(available_ingredients[j])
                clusteredCount = clusteredCount + 1

        words = []
        for entry in ingredient_cluster:
            words.extend(entry.name.split())
        common_words = set(words)
        for entry in ingredient_cluster:
            common_words = common_words.intersection(set(entry.name.split()))
        word_counts = Counter(words)
        common_word_counts = {word: count for word, count in word_counts.items() if word in common_words}
        sorted_words = sorted(common_word_counts.items(), key=lambda x: x[1], reverse=True)
        cluster_name = " ".join([x[0] for x in sorted_words])
        clustered_ingredients.append({
            'suggestedClusterName': cluster_name,
            'ingredients': [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredient_cluster]
        })

    return JsonResponse({'results': clustered_ingredients, 'clustered_count': clusteredCount, 'total_count': len(available_ingredients)})


@require_POST
@csrf_exempt
def confirmIngredientClusters(request):
    data = json.loads(request.body)
    clustered_ingredient_list = data['results']

    for clustered_ingredient in clustered_ingredient_list:
        suggested_cluster_name = clustered_ingredient['suggestedClusterName']
        ingredients = clustered_ingredient['ingredients']

        try:
            new_ingredient = NewIngredient.objects.get(name=suggested_cluster_name)
        except NewIngredient.DoesNotExist:
            new_ingredient = NewIngredient.objects.create(name=suggested_cluster_name)

        for ingredient in ingredients:
            ingredient_obj = Ingredient.objects.get(id=ingredient['id'])
            existing_synonym = IngredientSynonym.objects.filter(ingredient=ingredient_obj,
                                                                new_ingredient=new_ingredient).first()
            if not existing_synonym:
                ingredient_synonym = IngredientSynonym.objects.create(ingredient=ingredient_obj,
                                                                      new_ingredient=new_ingredient)

    return JsonResponse({'message': 'Successfully created new ingredients and ingredient synonyms.'})

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
