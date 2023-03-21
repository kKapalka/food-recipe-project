import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ClusteredIngredientList, ClusteredIngredient } from '../shared/models';

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
  confirmIngredientClusters(ingredientClusters: ClusteredIngredient[]) {
    return this.http.post<any>(`http://localhost:8000/ingredient-cluster/confirm`, {
      results: ingredientClusters
    });
  }


}
