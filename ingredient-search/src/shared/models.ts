export interface Ingredient {
  id: number;
  name: string;
  mergeClusterCandidate?: ClusteredIngredient;
}

export interface NewIngredient {
  id: number;
  name: string;
}

export interface IngredientList{
  results: Ingredient[];
}

export interface NewIngredientList{
  results: NewIngredient[];
}

export interface ClusteredIngredient{
  suggestedClusterName: string,
  ingredients: Ingredient[];
  mergeClusterCandidate?: ClusteredIngredient;
}

export interface ClusteredIngredientList {
  results: ClusteredIngredient[];
}
