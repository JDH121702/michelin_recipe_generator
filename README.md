# Michelin Star Recipe Generator

A desktop application that generates Michelin star recipes based on famous chefs like Thomas Keller, Niki Nakayama, Gordon Ramsay, and more. The application allows for extensive customization of recipes, including chef influence, Michelin star rating, ingredient types, and many other parameters.

## Features

- **Chef Selection**: Choose from multiple renowned Michelin-starred chefs and adjust their influence on the recipe
- **Michelin Star Rating**: Select between One, Two, or Three Michelin star complexity levels
- **Ingredient Options**: Toggle between everyday ingredients and luxurious, hard-to-find ingredients
- **Modern Gastronomy**: Adjust the level of modern/molecular gastronomy techniques
- **Dietary Restrictions**: Specify vegetarian, vegan, gluten-free, and other dietary needs
- **Occasion-based**: Optimize recipes for specific occasions like dinner parties or romantic dinners
- **Time Constraints**: Set preparation and cooking time limits
- **Equipment Selection**: Specify available cooking equipment
- **Comprehensive Recipes**: Receive detailed recipes with ingredients, instructions, chef notes, technique tips, and ingredient substitutions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies using one of these methods:

   **Option 1:** Using the installation script (recommended):
   ```bash
   python install_dependencies.py
   ```

   **Option 2:** Using pip with requirements file:
   ```bash
   pip install -r requirements.txt
   ```

   **Option 3:** Installing dependencies individually if you encounter errors:
   ```bash
   pip install PyQt5>=5.15.0
   pip install openai>=1.0.0
   pip install keyring>=23.0.0
   pip install pathlib>=1.0.1
   ```

4. Run the application:

```bash
python main.py
```

## OpenAI API Key

This application requires an OpenAI API key to generate recipes. You will be prompted to enter your API key when you first run the application. The key is stored securely using your system's keyring.

To obtain an API key:
1. Create an account at [OpenAI](https://openai.com/)
2. Navigate to the API section
3. Generate a new API key
4. Enter this key when prompted by the application

## Usage

1. **Chef Selection Tab**:
   - Select one or more chefs by checking the boxes
   - Adjust the influence sliders to determine how much each chef's style affects the recipe

2. **Recipe Parameters Tab**:
   - Choose the Michelin star rating (One, Two, or Three stars)
   - Select ingredient type (everyday or luxurious)
   - Adjust the modern gastronomy slider
   - Toggle specialized equipment if available

3. **Dietary & Occasion Tab**:
   - Select any dietary restrictions
   - Choose the occasion for the recipe
   - Set the number of servings

4. **Equipment & Time Tab**:
   - Set preparation and cooking time constraints
   - Select available cooking equipment

5. Click the "Generate Michelin Recipe" button to create your custom recipe

6. The generated recipe will appear in the right panel with options to save or export

## Saving and Exporting Recipes

- **Save Recipe**: Save the recipe as a JSON or HTML file
- **Export as PDF**: Export the recipe as a PDF document (coming soon)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the culinary excellence of Michelin-starred chefs
- UI design inspired by Black Desert Online's character customization interface