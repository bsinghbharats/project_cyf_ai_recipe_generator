from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from generator import RecipeGenerator
import os
import json

class ActionGenerateRecipe(Action):
    def name(self) -> Text:
        return "action_generate_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get slots
        ingredients = tracker.get_slot("available_ingredients") or []
        dietary_restrictions = tracker.get_slot("dietary_restrictions") or []
        
        # Generate recipe
        generator = RecipeGenerator(r"C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json")
        recipes = generator.find_similar_recipes(ingredients, dietary_restrictions)
        
        if recipes:
            recipe = recipes[0]  # Get top match
            response = f"Here's a recipe for {recipe['Title']}:\n\n"
            response += "Ingredients:\n- " + "\n- ".join(recipe['Cleaned_Ingredients']) + "\n\n"
            response += "Instructions:\n" + recipe['Instructions']
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I couldn't find a recipe matching your ingredients and restrictions.")
        
        return []

class ActionSuggestVariation(Action):
    def name(self) -> Text:
        return "action_suggest_variation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get last recipe mentioned
        # In a real app, you'd want to track this better
        generator = RecipeGenerator(r"C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json")
        last_recipe_title = next(tracker.get_latest_entity_values("recipe_type"), None)
        
        if last_recipe_title:
            # Find the full recipe (simplified - in real app you'd have better lookup)
            with open(os.path.join(r"C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json"), 'r') as f:
                for line in f:
                    recipe = json.loads(line)
                    if recipe['Title'] == last_recipe_title:
                        variation = generator.suggest_variation(recipe)
                        if variation:
                            response = f"How about trying this variation: {variation['Title']}\n\n"
                            response += "Ingredients:\n- " + "\n- ".join(variation['Cleaned_Ingredients'])
                            dispatcher.utter_message(text=response)
                            return []
        
        dispatcher.utter_message(text="I couldn't find a variation. Maybe try different ingredients?")
        return []