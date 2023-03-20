export interface Ingredient {
  id: number;
  name: string;
  newIngredient?: NewIngredient;
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
}

export interface ClusteredIngredientList {
  results: ClusteredIngredient[];
}
