AI Recipe Generator
===================
A smart cooking assistant powered by Python, SpaCy, and Rasa that generates personalized recipes based on ingredients and dietary restrictions.

Features
--------
- Natural Language Understanding for queries like "vegetarian recipe with potatoes"
- Ingredient matching using TF-IDF + cosine similarity
- Dietary filters (vegetarian/vegan/gluten-free)
- Conversational interface with Rasa
- Recipe variation suggestions

Tech Stack
----------
- NLP: SpaCy (entity recognition)
- Dialog: Rasa (conversation flow)
- Backend: Python
- Data: Pandas
- Vectorization: Scikit-learn

Repository Structure
--------------------
recipe_generator/
├── data/                   # Recipe datasets
│   ├── raw_recipes.csv     # Original dataset
│   └── processed_recipes.json  # Cleaned data
├── models/                 # Trained models
│   ├── nlp_model/          # SpaCy NLP model
│   └── rasa_model/         # Rasa dialogue model
├── rasa/                   # Rasa config files
│   ├── actions/            # Custom actions
│   ├── data/               # NLU/stories/rules
│   ├── config.yml          # Pipeline settings
│   └── domain.yml          # Bot responses
├── app/                    # Core logic
│   ├── generator.py        # Recipe matching
│   └── server.py           # Flask API
└── tests/                  # Unit tests

Installation
------------
1. Prerequisites:
   - Python 3.8+
   - Git
   - Graphviz (for visualization)

2. Clone repo:
   git clone [https://github.com/yourusername/ai-recipe-generator.git](https://github.com/bsinghbharats/project_cyf_ai_recipe_generator.git)
   cd ai-recipe-generator

3. Setup environment:
   python -m venv venv
   venv\Scripts\activate (Windows)
   source venv/bin/activate (Linux/Mac)

4. Install dependencies:
   pip install -r requirements.txt
   python -m spacy download en_core_web_md

Running the Project
------------------
Option 1: Command Line Chat
1. Start Rasa actions server:
   rasa run actions

2. Launch bot:
   rasa shell

Try queries:
- "I need a vegan recipe with tofu"
- "What can I make with chicken and rice?"

Option 2: Flask API
python app/server.py

API Endpoints:
- POST /generate
  {"ingredients": ["potatoes"], "dietary_restrictions": ["vegetarian"]}
- POST /variation
  {"title": "Vegetable Curry"}

Training Models
--------------
1. Preprocess data:
   python app/preprocess.py

2. Train SpaCy model:
   python app/train_nlp.py

3. Train Rasa model:
   cd rasa
   rasa train

Testing
-------
- Unit tests:
  pytest tests/
- Validate data:
  rasa data validate
- Visualize:
  rasa visualize

Dataset Details
--------------
Columns Used:
- Title: Recipe name
- Cleaned_Ingredients: Preprocessed list
- Instructions: Cooking steps

Sample Entry:
{
  "Title": "Vegetable Curry",
  "Cleaned_Ingredients": ["potatoes", "carrots"],
  "Instructions": "1. Chop vegetables...",
  "Image_Name": "curry.jpg"
}

Debugging Tips
-------------
1. No bot response?
   - Check rasa run actions is running
   - Verify domain.yml slot mappings

2. Entity extraction failing?
   python app/train_nlp.py --epochs 50

3. Rasa errors?
   rasa data validate --debug

License
-------
MIT License

Contribution
------------
1. Fork project
2. Add recipes to data/raw_recipes.csv
3. Improve NLP training data
4. Submit PR

Suggested Improvements:
- Calorie calculation
- Spoonacular API integration
- React frontend
