import os
import json
import time
from datetime import datetime
from openai import OpenAI
from html import escape

class RecipeGenerator:
    """
    Handles recipe generation using the OpenAI API based on user parameters.
    Constructs prompts, processes API responses, and formats recipes.
    """

    def __init__(self, settings_manager):
        """Initialize the recipe generator with settings manager"""
        self.settings_manager = settings_manager
        self.setup_api()

    def setup_api(self):
        """Set up the OpenAI API client with the stored API key"""
        api_key = self.settings_manager.get_api_key()
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def generate_recipe(self, params):
        """Generate a recipe based on the provided parameters"""
        # Check if API client is set
        if not hasattr(self, 'client') or self.client is None:
            raise ValueError("OpenAI API key is not set. Please set it in the settings.")

        # Construct the prompt
        prompt = self._construct_prompt(params) # Call _construct_prompt

        # Get API settings
        model = self.settings_manager.get_setting("api_settings.model", "gpt-4")
        temperature = self.settings_manager.get_setting("api_settings.temperature", 0.7)
        max_tokens = self.settings_manager.get_setting("api_settings.max_tokens", 2000)

        try: # Outer try block for the whole generation process
            # Call the OpenAI API using the new client interface
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_completion_tokens=max_tokens # Use max_completion_tokens instead of max_tokens
            )

            recipe_text = None # Initialize recipe_text
            try: # Inner try block specifically for response processing
                # Process the response with validation
                if not response or not response.choices:
                    raise Exception("Invalid response received from API: No choices found.")

                first_choice = response.choices[0]
                if not first_choice:
                    raise Exception("Invalid response received from API: No first choice found.")

                # Safely access message and content using getattr
                message_obj = getattr(first_choice, 'message', None)
                if not message_obj:
                    raise Exception("Invalid response received from API: No message object found.")

                recipe_text = getattr(message_obj, 'content', None)

                if not recipe_text:
                     raise Exception("Invalid response received from API: Message content is empty.")

            except Exception as resp_err:
                 # Print details if response processing fails (optional)
                 # print(f"ERROR processing API response: {resp_err}")
                 # print(f"Response object type: {type(response)}")
                 raise Exception(f"Failed to process API response: {resp_err}") from resp_err

            # Continue if response processing succeeded and recipe_text is valid
            recipe = self._process_recipe(recipe_text, params)

            # Save to history if enabled
            self.settings_manager.save_recipe_to_history(recipe)

            return recipe

        except Exception as e: # Catch errors from API call or response processing re-raise
            raise Exception(f"Error generating recipe: {str(e)}") from e

    def _get_system_prompt(self):
        """Get the system prompt for the OpenAI API"""
        return """
        You are a world-class culinary AI specializing in Michelin-star level recipes.
        Your expertise spans various chef styles, techniques, and cuisines.

        Create detailed, professional recipes that include:
        1. A creative and descriptive title
        2. A brief introduction explaining the dish and its inspiration
        3. Comprehensive ingredients list with precise measurements
        4. Detailed preparation instructions broken down by components
        5. Step-by-step cooking instructions with timing and technique details
        6. Plating instructions with artistic presentation guidance
        7. Chef's notes with technique tips and insights
        8. Suggested wine or beverage pairings
        9. Possible ingredient substitutions

        Format your response in a clean, structured way that a professional chef would appreciate,
        while ensuring it's understandable for home cooks. Include specific techniques relevant to
        the chef styles requested.
        """

    def _construct_prompt(self, params):
        """Construct a detailed prompt based on the parameters"""
        # Start with basic prompt
        prompt = "Create a Michelin-star level recipe with the following specifications:\n\n"

        # Add chef influences
        if params["chefs"]:
            prompt += "CHEF INFLUENCES:\n"
            # Import locally to avoid potential circular dependency if CHEF_PROFILES needs RecipeGenerator
            from .chef_profiles import CHEF_PROFILES, CHEF_INFLUENCE_DESCRIPTIONS
            for chef_id, influence in params["chefs"].items():
                chef = CHEF_PROFILES.get(chef_id, {})

                # Determine influence level
                influence_level = "low"
                if influence >= 70:
                    influence_level = "high"
                elif influence >= 30:
                    influence_level = "medium"

                influence_desc = CHEF_INFLUENCE_DESCRIPTIONS.get(chef_id, {}).get(influence_level, "")

                prompt += f"- {chef.get('name', 'Unknown Chef')} ({influence}% influence): {influence_desc}\n"
                prompt += f"  Known for: {chef.get('signature', '')}\n"
        else:
            prompt += "CHEF INFLUENCES: No specific chef selected. Create a general Michelin-star level recipe.\n"

        # Add Michelin star rating
        prompt += f"\nMICHELIN STAR LEVEL: {params['michelin_stars']} star"
        if params['michelin_stars'] == 1:
            prompt += " - Excellent cooking, worth a stop"
        elif params['michelin_stars'] == 2:
            prompt += " - Excellent cooking, worth a detour"
        elif params['michelin_stars'] == 3:
            prompt += " - Exceptional cuisine, worth a special journey"
        prompt += "\n"

        # Add ingredient type
        prompt += f"\nINGREDIENT TYPE: "
        if params['ingredient_type'] == 'everyday':
            prompt += "Everyday ingredients that are commonly available in well-stocked supermarkets"
        else:
            prompt += "Luxurious, hard-to-find ingredients that might require specialty stores or online ordering"

        if params['seasonal']:
            prompt += "\nPrioritize seasonal ingredients appropriate for the current time of year"
        prompt += "\n"

        # Add gastronomy level
        prompt += f"\nGASTRONOMY LEVEL: {params['gastronomy_level']}% modern techniques"
        if params['gastronomy_level'] < 30:
            prompt += " (mostly traditional cooking methods)"
        elif params['gastronomy_level'] > 70:
            prompt += " (significant use of molecular gastronomy and modern techniques)"
        else:
            prompt += " (balanced mix of traditional and modern techniques)"

        if params['specialized_equipment']:
            prompt += "\nSpecialized equipment is available (sous vide, anti-griddle, etc.)"
        prompt += "\n"

        # Add dietary restrictions
        if params['dietary_restrictions']:
            prompt += "\nDIETARY RESTRICTIONS: " + ", ".join(params['dietary_restrictions']) + "\n"

        # Add occasion
        prompt += f"\nOCCASION: {params['occasion']}\n"

        # Add servings
        prompt += f"\nSERVINGS: {params['servings']}\n"

        # Add time constraints
        prompt += f"\nTIME CONSTRAINTS:"
        prompt += f"\n- Preparation time: approximately {params['prep_time']} minutes"
        prompt += f"\n- Cooking time: approximately {params['cook_time']} minutes\n"

        # Add available equipment
        if params['equipment']:
            prompt += "\nAVAILABLE EQUIPMENT: " + ", ".join(params['equipment']) + "\n"

        # Final instructions
        prompt += """
        \nPlease create a comprehensive recipe that includes:
        1. A creative and descriptive title
        2. A brief introduction explaining the dish and its inspiration
        3. Comprehensive ingredients list with precise measurements
        4. Detailed preparation instructions broken down by components
        5. Step-by-step cooking instructions with timing and technique details
        6. Plating instructions with artistic presentation guidance
        7. Chef's notes with technique tips and insights
        8. Suggested wine or beverage pairings
        9. Possible ingredient substitutions

        The recipe should reflect the chef influences, Michelin star level, and all other parameters specified above.
 
        Finally, at the very end of your response, include a line formatted exactly like this:
        **Complexity Score: [score]/10**
        Where [score] is an integer from 1 to 10 representing the overall complexity based on ingredients and techniques.
        """
        return prompt

    def _process_recipe(self, recipe_text, params):
        import re # Import regex module
        """Process the raw recipe text into a structured format"""
        # Create recipe object
        recipe = {
            "raw_text": recipe_text,
            "html_content": self._format_recipe_as_html(recipe_text),
            "parameters": params,
            "timestamp": datetime.now().isoformat(),
            "id": f"recipe_{int(time.time())}",
            "complexity_score": "N/A" # Add default score
        }

        # Try to extract title
        lines = recipe_text.split('\n')
        if lines and lines[0].strip():
            recipe["title"] = lines[0].strip()
        else:
            recipe["title"] = "Michelin Star Recipe"

        # Try to extract complexity score
        score_match = re.search(r"\*\*Complexity Score:\s*(\d{1,2})/10\*\*", recipe_text)
        if score_match:
            try:
                score = int(score_match.group(1))
                if 1 <= score <= 10:
                    recipe["complexity_score"] = f"{score}/10"
                    # Optional: Remove the score line from the raw text if desired
                    # recipe_text = re.sub(r"\*\*Complexity Score:\s*\d{1,2}/10\*\*\n?", "", recipe_text).strip()
                    # recipe["raw_text"] = recipe_text # Update raw text if removing score line
                    # recipe["html_content"] = self._format_recipe_as_html(recipe_text) # Re-format HTML if removing score line
            except ValueError:
                pass # Ignore if score is not a valid integer

        return recipe

    def _format_recipe_as_html(self, recipe_text):
        """Format the recipe text as HTML for display"""
        # Basic HTML structure
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #F0F0F0; /* Light base text color */
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #FFFFFF; /* White for main title */
                    font-size: 28px;
                    margin-bottom: 10px;
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #E0E0E0; /* Lighter gray for h2 */
                    font-size: 22px;
                    margin-top: 25px;
                    margin-bottom: 10px;
                }
                h3 {
                    color: #D0D0D0; /* Lighter gray for h3 */
                    font-size: 18px;
                    margin-top: 20px;
                    margin-bottom: 8px;
                }
                p {
                    margin-bottom: 15px;
                }
                ul, ol {
                    margin-bottom: 20px;
                    padding-left: 25px;
                }
                li {
                    margin-bottom: 8px;
                }
                .section {
                    margin-bottom: 30px;
                }
                .chef-notes {
                    background-color: #f9f9f9;
                    border-left: 4px solid #ddd;
                    padding: 15px;
                    margin: 20px 0;
                }
                .substitutions {
                    background-color: #f5f5f5;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 5px;
                }
                .wine-pairing {
                    font-style: italic;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
        """

        # Process the recipe text
        lines = recipe_text.strip().split('\n')
        in_list = False
        list_type = None

        for i, line in enumerate(lines):
            line = line.strip()

            # Skip empty lines
            if not line:
                if in_list:
                    html += "</ul>\n" if list_type == "ul" else "</ol>\n"
                    in_list = False
                    list_type = None
                html += "<p>&nbsp;</p>\n"
                continue

            # Check if this is a title (first line)
            if i == 0:
                html += f"<h1>{escape(line)}</h1>\n"
                continue

            # Check if this is a section header
            if line.isupper() or (line.endswith(':') and len(line) < 50):
                if in_list:
                    html += "</ul>\n" if list_type == "ul" else "</ol>\n"
                    in_list = False
                    list_type = None

                # Clean up the header
                header = line.rstrip(':').title()

                # Apply specific styling based on section
                if "INGREDIENTS" in line.upper():
                    html += f"<h2>{escape(header)}</h2>\n"
                elif "INSTRUCTIONS" in line.upper() or "DIRECTIONS" in line.upper() or "METHOD" in line.upper():
                    html += f"<h2>{escape(header)}</h2>\n"
                elif "NOTES" in line.upper() or "TIPS" in line.upper():
                    html += f'<div class="chef-notes"><h2>{escape(header)}</h2>\n'
                elif "SUBSTITUTIONS" in line.upper() or "ALTERNATIVES" in line.upper():
                    html += f'<div class="substitutions"><h2>{escape(header)}</h2>\n'
                elif "WINE" in line.upper() or "PAIRING" in line.upper():
                    html += f'<div class="wine-pairing"><h2>{escape(header)}</h2>\n'
                elif "PLATING" in line.upper() or "PRESENTATION" in line.upper():
                    html += f"<h2>{escape(header)}</h2>\n"
                else:
                    html += f"<h3>{escape(header)}</h3>\n"

                continue

            # Check if this is a list item
            if line.startswith('-') or line.startswith('•') or (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and ' ' in line):
                # Determine list type
                new_list_type = "ul" if line.startswith(('-', '•')) else "ol"

                # Start a new list if needed
                if not in_list or list_type != new_list_type:
                    if in_list:
                        html += "</ul>\n" if list_type == "ul" else "</ol>\n"
                    html += "<ul>\n" if new_list_type == "ul" else "<ol>\n"
                    in_list = True
                    list_type = new_list_type

                # Clean up the list item
                item = line[1:].strip() if line.startswith(('-', '•')) else line[line.find('.')+1:].strip()
                html += f"<li>{escape(item)}</li>\n"
            else:
                # Regular paragraph
                if in_list:
                    html += "</ul>\n" if list_type == "ul" else "</ol>\n"
                    in_list = False
                    list_type = None

                html += f"<p>{escape(line)}</p>\n"

        # Close any open lists
        if in_list:
            html += "</ul>\n" if list_type == "ul" else "</ol>\n"

        # Close any open divs
        # Note: This logic might be flawed if divs aren't properly nested in the input text
        open_notes = html.count('<div class="chef-notes">')
        open_subs = html.count('<div class="substitutions">')
        open_wine = html.count('<div class="wine-pairing">')
        closed_divs = html.count('</div>')

        # Heuristic: Close divs based on counts, might need refinement
        if open_notes > closed_divs: html += "</div>\n" * (open_notes - closed_divs)
        closed_divs = html.count('</div>') # Recount
        if open_subs > closed_divs: html += "</div>\n" * (open_subs - closed_divs)
        closed_divs = html.count('</div>') # Recount
        if open_wine > closed_divs: html += "</div>\n" * (open_wine - closed_divs)


        # Close HTML
        html += """
        </body>
        </html>
        """

        return html