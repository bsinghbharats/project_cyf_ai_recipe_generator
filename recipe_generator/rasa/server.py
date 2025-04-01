from flask import Flask, request, jsonify
from recipe_generator.rasa.generator import RecipeGenerator
import os
import json

app = Flask(__name__)
generator = RecipeGenerator(r"C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json")

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get('ingredients', [])
    dietary_restrictions = data.get('dietary_restrictions', [])
    
    recipes = generator.find_similar_recipes(ingredients, dietary_restrictions)
    if recipes:
        return jsonify(recipes[0])
    return jsonify({"error": "No recipes found"}), 404

@app.route('/variation', methods=['POST'])
def suggest_variation():
    data = request.json
    recipe_title = data.get('title', '')
    
    # Find the recipe (simplified)
    with open(os.path.join(r"C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json"), 'r') as f:
        for line in f:
            recipe = json.loads(line)
            if recipe['Title'] == recipe_title:
                variation = generator.suggest_variation(recipe)
                if variation:
                    return jsonify(variation)
                break
    
    return jsonify({"error": "No variation found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)