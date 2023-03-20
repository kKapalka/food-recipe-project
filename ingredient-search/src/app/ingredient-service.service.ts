import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ClusteredIngredientList, Ingredient, IngredientList, NewIngredient, NewIngredientList } from '../shared/models';

@Injectable({
  providedIn: 'root'
})
export class IngredientServiceService {


  constructor(private http: HttpClient) {}

  getClusteredIngredients(name: string, epsilon: number, minSamples: number) {
    return this.http.post<ClusteredIngredientList>(`http://localhost:8000/ingredient-cluster`, {
      name: name,
      epsilon: epsilon,
      min_samples: minSamples
    });

  }

  getNewIngredients(): Observable<NewIngredientList> {
    return this.http.get<IngredientList>('http://localhost:8000/new-ingredients/search');
  }

  searchIngredients(keyword: string, selectedIngredientId: number): Observable<IngredientList>{
    const url = `http://localhost:8000/ingredients/search`;
    return this.http.post<IngredientList>(url, {keyword: keyword, newIngredientId: selectedIngredientId})
  }

  createNewIngredient(name: string): Observable<NewIngredient>{
    const url = `http://localhost:8000/new-ingredient/`;
    return this.http.post<Ingredient>(url, {name: name});
  }

  createIngredientSynonym(ingredientId: number, newIngredientId: number): Observable<NewIngredient>{
    const url = `http://localhost:8000/synonym/`;
    return this.http.post<Ingredient>(url, {ingredientId: ingredientId, newIngredientId: newIngredientId});
  }

  searchRelatedIngredients(newIngredientId: number): Observable<IngredientList>{
    const url = `http://localhost:8000/related-ingredients/search?newIngredientId=${newIngredientId}`;
    return this.http.get<IngredientList>(url);
  }

}
