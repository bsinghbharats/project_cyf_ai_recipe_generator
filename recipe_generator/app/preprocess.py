import pandas as pd
import json
import spacy
from sklearn.model_selection import train_test_split

nlp = spacy.load("en_core_web_sm")

def preprocess_data(input_path, output_path):
    # Load data
    df = pd.read_csv(input_path)
    
    # Drop unnecessary columns and rows with missing values
    df = df.drop(columns=['Unnamed: 0'])
    df = df.dropna(subset=['Title', 'Ingredients', 'Instructions'])
    
    # Process ingredients
    df['Cleaned_Ingredients'] = df['Ingredients'].apply(lambda x: [ing.strip() for ing in x.split(',')])
    
    # Tokenize instructions
    df['Tokenized_Instructions'] = df['Instructions'].apply(lambda x: [sent.text for sent in nlp(x).sents])
    
    # Save processed data
    df.to_json(output_path, orient='records', lines=True)
    
    # Split for training/testing
    train, test = train_test_split(df, test_size=0.2)
    return train, test

if __name__ == "__main__":
    train, test = preprocess_data(r'C:\Users\singh\Documents\Project_CY\recipe_generator\data\raw_recipes.csv', r'C:\Users\singh\Documents\Project_CY\recipe_generator\data\processed_recipes.json')
    print(f"Preprocessing complete. Train: {len(train)}, Test: {len(test)}")