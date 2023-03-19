import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ingredient, IngredientList, NewIngredient, NewIngredientList } from '../shared/models';

@Injectable({
  providedIn: 'root'
})
export class IngredientServiceService {


  constructor(private http: HttpClient) {}

  getNewIngredients(): Observable<NewIngredientList> {
    return this.http.get<IngredientList>('http://localhost:8000/new-ingredients/search');
  }

  searchIngredients(searchQuery: string): Observable<IngredientList>{
    const url = `http://localhost:8000/ingredients/search?query=${encodeURIComponent(searchQuery)}`;
    return this.http.get<IngredientList>(url)
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
