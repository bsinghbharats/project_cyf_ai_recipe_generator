import json
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecipeGenerator:
    def __init__(self, data_path):
        with open(data_path, 'r') as f:
            self.recipes = [json.loads(line) for line in f]
        
        # Prepare TF-IDF for ingredients
        self.ingredient_vectorizer = TfidfVectorizer()
        self.ingredient_matrix = self.ingredient_vectorizer.fit_transform(
            [' '.join(recipe['Cleaned_Ingredients']) for recipe in self.recipes]
        )
        
        # Prepare TF-IDF for titles
        self.title_vectorizer = TfidfVectorizer()
        self.title_matrix = self.title_vectorizer.fit_transform(
            [recipe['Title'] for recipe in self.recipes]
        )

    def find_similar_recipes(self, ingredients, dietary_restrictions=None, n=5):
        # Vectorize input ingredients
        input_vec = self.ingredient_vectorizer.transform([' '.join(ingredients)])
        
        # Calculate similarity
        sim_scores = cosine_similarity(input_vec, self.ingredient_matrix)
        top_indices = sim_scores.argsort()[0][-n:][::-1]
        
        # Filter by dietary restrictions if provided
        if dietary_restrictions:
            filtered_recipes = []
            for idx in top_indices:
                recipe = self.recipes[idx]
                if self._matches_dietary(recipe, dietary_restrictions):
                    filtered_recipes.append(recipe)
            return filtered_recipes[:n]
        
        return [self.recipes[idx] for idx in top_indices]

    def _matches_dietary(self, recipe, restrictions):
        # Simple check - in a real app you'd want more sophisticated checks
        ingredients_text = ' '.join(recipe['Cleaned_Ingredients']).lower()
        for restriction in restrictions:
            if restriction.lower() == 'vegetarian':
                non_veg = ['meat', 'chicken', 'beef', 'pork', 'fish']
                if any(ing in ingredients_text for ing in non_veg):
                    return False
            elif restriction.lower() == 'vegan':
                non_vegan = ['meat', 'chicken', 'beef', 'pork', 'fish', 'dairy', 'milk', 'cheese', 'egg']
                if any(ing in ingredients_text for ing in non_vegan):
                    return False
        return True

    def suggest_variation(self, recipe):
        # Find similar recipes by title
        input_vec = self.title_vectorizer.transform([recipe['Title']])
        sim_scores = cosine_similarity(input_vec, self.title_matrix)
        top_indices = sim_scores.argsort()[0][-5:][::-1]
        
        # Exclude the original recipe
        variations = [self.recipes[idx] for idx in top_indices if self.recipes[idx]['Title'] != recipe['Title']]
        return variations[0] if variations else None