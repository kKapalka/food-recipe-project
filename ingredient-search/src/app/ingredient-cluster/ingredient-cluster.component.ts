import { Component, OnInit, Input } from '@angular/core';
import { IngredientServiceService } from '../ingredient-service.service';
import { Ingredient, ClusteredIngredient } from '../../shared/models';

@Component({
  selector: 'app-ingredient-cluster',
  templateUrl: './ingredient-cluster.component.html',
  styleUrls: ['./ingredient-cluster.component.css']
})
export class IngredientClusterComponent implements OnInit {

  clusteredIngredients: ClusteredIngredient[] = [];
  detachedIngredients: Ingredient[] = [];

  ingredientName: string = '';
  epsilon: number = 0.5;
  minClusterSize: number = 2;

  constructor(private ingredientService: IngredientServiceService) { }

  getClusteredIngredients() {
    this.ingredientService.getClusteredIngredients(this.ingredientName, this.epsilon, this.minClusterSize).subscribe(result => {
      this.clusteredIngredients = result.results;
    });
  }

  removeCluster(clusteredIngredient: ClusteredIngredient) {
    this.clusteredIngredients.splice(this.clusteredIngredients.indexOf(clusteredIngredient), 1);
    this.detachedIngredients = this.detachedIngredients.concat(clusteredIngredient.ingredients);
  }

  mergeClusters(clusteredIngredient: ClusteredIngredient, otherClusterName: string) {
    const otherCluster = this.clusteredIngredients.find(ci => ci.suggestedClusterName === otherClusterName);
    if (otherCluster) {
      otherCluster.ingredients = otherCluster.ingredients.concat(clusteredIngredient.ingredients);
      this.clusteredIngredients.splice(this.clusteredIngredients.indexOf(clusteredIngredient), 1);
    }
  }

  detachIngredient(clusteredIngredient: ClusteredIngredient, ingredientToDetach: Ingredient) {
    this.detachedIngredients.push(ingredientToDetach);
    this.clusteredIngredients.find(ci => ci.suggestedClusterName === clusteredIngredient.suggestedClusterName)!.ingredients.splice(clusteredIngredient.ingredients.indexOf(ingredientToDetach), 1);
  }

  attachIngredient(clusteredIngredient: ClusteredIngredient, ingredientToAttach: Ingredient) {
    this.clusteredIngredients.find(ci => ci.suggestedClusterName === clusteredIngredient.suggestedClusterName)!.ingredients.push(ingredientToAttach);
    this.detachedIngredients.splice(this.detachedIngredients.indexOf(ingredientToAttach), 1);
  }

  ngOnInit(): void {
  }

}
