import spacy
import random
from spacy.training.example import Example
import json
import os
import time
from tqdm import tqdm  # Import tqdm for the progress bar

# Load the dataset from a JSON file
def load_data(filepath):
    with open(filepath, 'r') as f:
        data = [json.loads(line) for line in f]
    return data

# Prepare training data in the format SpaCy expects
def prepare_training_data(data):
    TRAIN_DATA = []
    for recipe in data:
        # Teach the model to recognize recipe titles as entities
        entities = [(0, len(recipe['Title']), "RECIPE")]
        TRAIN_DATA.append((recipe['Title'], {"entities": entities}))
        
        # Teach the model to recognize ingredients as entities
        for ingredient in recipe['Cleaned_Ingredients']:
            entities = [(0, len(ingredient), "INGREDIENT")]
            TRAIN_DATA.append((ingredient, {"entities": entities}))
    return TRAIN_DATA

# Optimized training function
def train_spacy_model(TRAIN_DATA, output_dir):
    # Check if GPU is available and prefer GPU
    if spacy.prefer_gpu():
        spacy.require_gpu()
        print("Using GPU for training.")
    else:
        print("Using CPU for training.")
    
    # Create a blank English model
    nlp = spacy.blank("en")
    
    # Add entity recognizer to the pipeline if it's not already there
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    
    # Add labels for RECIPE and INGREDIENT
    ner.add_label("RECIPE")
    ner.add_label("INGREDIENT")
    
    # Disable other pipelines to speed up training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    # Start training
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        start_time = time.time()
        
        # Train for a set number of iterations, reduce iterations for speed during testing
        for itn in range(20):  # Use fewer iterations for debugging, increase as needed
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            # Batch processing for faster training
            # For this example, we are training on the whole dataset at once; you can experiment with batch size.
            batch_size = 16  # Adjust batch size for better speed
            batch_progress = tqdm(range(0, len(TRAIN_DATA), batch_size), desc=f"Iteration {itn + 1}")
            
            for i in batch_progress:
                batch = TRAIN_DATA[i:i + batch_size]
                examples = []
                for text, annotations in batch:
                    example = Example.from_dict(nlp.make_doc(text), annotations)
                    examples.append(example)
                nlp.update(examples, drop=0.3, losses=losses)  # Dropout rate set to 0.3 for speed
                
                # Update the progress bar description
                batch_progress.set_postfix(loss=losses.get("ner", "N/A"))
            
            print(f"Iteration {itn + 1}, Losses: {losses}")
        
        end_time = time.time()
        print(f"Training completed in {end_time - start_time:.2f} seconds.")
    
    # Save the trained model
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    # Load the preprocessed recipe data (adjust the path to your file)
    data = load_data(r'C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json')
    
    # Prepare training data
    TRAIN_DATA = prepare_training_data(data[:500])  # Reduce data size for faster experimentation (e.g., use 500 samples)
    
    # Train the model
    output_dir = r'C:\Users\singh\Documents\Project_CY\recipe_generator\models\nlp_model'
    train_spacy_model(TRAIN_DATA, output_dir)
