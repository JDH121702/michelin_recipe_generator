import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                            QVBoxLayout, QHBoxLayout, QLabel, QSlider,
                            QPushButton, QComboBox, QCheckBox, QSpinBox,
                            QTextEdit, QGroupBox, QRadioButton, QScrollArea,
                            QSplitter, QFrame, QFileDialog, QMessageBox,
                            QDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon

# Import custom modules
from chef_profiles import CHEF_PROFILES
from recipe_generator import RecipeGenerator
from settings_manager import SettingsManager
from api_key_dialog import ApiKeyDialog

class MichelinRecipeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize settings
        self.settings_manager = SettingsManager()
        self.recipe_generator = RecipeGenerator(self.settings_manager)
        
        # Check for API key
        self.check_api_key()
        
        # Setup UI
        self.init_ui()
        
    def check_api_key(self):
        """Check if an API key is set and prompt if not"""
        if not self.settings_manager.has_api_key():
            dialog = ApiKeyDialog(self.settings_manager)
            result = dialog.exec_()
            
            if result == QDialog.Accepted:
                # API key was set
                self.recipe_generator.setup_api()
            else:
                # User cancelled, show warning
                QMessageBox.warning(
                    self,
                    "API Key Required",
                    "An OpenAI API key is required to generate recipes. "
                    "You can set it later in the settings."
                )
    
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Michelin Star Recipe Generator")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Create left panel (customization options)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create tab widget for customization categories
        self.tabs = QTabWidget()
        
        # Create tabs
        self.chef_tab = self.create_chef_tab()
        self.recipe_params_tab = self.create_recipe_params_tab()
        self.dietary_occasion_tab = self.create_dietary_occasion_tab()
        self.equipment_time_tab = self.create_equipment_time_tab()
        
        # Add tabs to tab widget
        self.tabs.addTab(self.chef_tab, "Chef Selection")
        self.tabs.addTab(self.recipe_params_tab, "Recipe Parameters")
        self.tabs.addTab(self.dietary_occasion_tab, "Dietary & Occasion")
        self.tabs.addTab(self.equipment_time_tab, "Equipment & Time")
        
        # Add generate button
        generate_button = QPushButton("Generate Michelin Recipe")
        generate_button.setMinimumHeight(50)
        generate_button.setFont(QFont("Arial", 12, QFont.Bold))
        generate_button.clicked.connect(self.generate_recipe)
        
        # Add widgets to left layout
        left_layout.addWidget(self.tabs)
        left_layout.addWidget(generate_button)
        
        # Create right panel (recipe display)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Create recipe display
        self.recipe_display = QTextEdit()
        self.recipe_display.setReadOnly(True)
        self.recipe_display.setFont(QFont("Arial", 11))
        
        # Add save and export buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Recipe")
        export_button = QPushButton("Export as PDF")
        save_button.clicked.connect(self.save_recipe)
        export_button.clicked.connect(self.export_recipe)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(export_button)
        
        # Add widgets to right layout
        right_layout.addWidget(QLabel("Generated Recipe"))
        right_layout.addWidget(self.recipe_display)
        right_layout.addLayout(button_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial sizes
        splitter.setSizes([400, 800])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Show welcome message
        self.show_welcome_message()
        
    def create_chef_tab(self):
        """Create the chef selection tab with influence sliders"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Add description
        description = QLabel("Select chefs and adjust their influence on the recipe")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Create scrollable area for chef selection
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Chef selection widgets
        self.chef_sliders = {}
        self.chef_checkboxes = {}
        
        for chef_id, chef_info in CHEF_PROFILES.items():
            # Create group box for each chef
            chef_group = QGroupBox(chef_info['name'])
            chef_layout = QVBoxLayout()
            
            # Add chef description
            chef_desc = QLabel(f"Style: {chef_info['style']}\nSignature: {chef_info['signature']}")
            chef_desc.setWordWrap(True)
            chef_layout.addWidget(chef_desc)
            
            # Add checkbox for selection
            checkbox = QCheckBox("Include this chef's influence")
            self.chef_checkboxes[chef_id] = checkbox
            chef_layout.addWidget(checkbox)
            
            # Add slider for influence
            slider_layout = QHBoxLayout()
            slider_layout.addWidget(QLabel("Influence:"))
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(0)
            slider.setEnabled(False)  # Disabled until checkbox is checked
            self.chef_sliders[chef_id] = slider
            
            # Add value label
            value_label = QLabel("0%")
            
            # Connect signals
            checkbox.stateChanged.connect(lambda state, s=slider: s.setEnabled(state))
            slider.valueChanged.connect(lambda value, label=value_label: label.setText(f"{value}%"))
            
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)
            chef_layout.addLayout(slider_layout)
            
            # Set layout for group box
            chef_group.setLayout(chef_layout)
            scroll_layout.addWidget(chef_group)
        
        # Add spacer at the end
        scroll_layout.addStretch()
        
        # Set scroll content and add to layout
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return tab
    
    def create_recipe_params_tab(self):
        """Create the recipe parameters tab with Michelin star rating and ingredient options"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Michelin Star Rating
        star_group = QGroupBox("Michelin Star Rating")
        star_layout = QVBoxLayout()
        
        # Radio buttons for star rating
        self.one_star_radio = QRadioButton("One Star - Excellent cooking, worth a stop")
        self.two_star_radio = QRadioButton("Two Stars - Excellent cooking, worth a detour")
        self.three_star_radio = QRadioButton("Three Stars - Exceptional cuisine, worth a special journey")
        
        # Set default
        self.one_star_radio.setChecked(True)
        
        star_layout.addWidget(self.one_star_radio)
        star_layout.addWidget(self.two_star_radio)
        star_layout.addWidget(self.three_star_radio)
        star_group.setLayout(star_layout)
        layout.addWidget(star_group)
        
        # Ingredient Type
        ingredient_group = QGroupBox("Ingredient Type")
        ingredient_layout = QVBoxLayout()
        
        # Radio buttons for ingredient type
        self.everyday_radio = QRadioButton("Everyday Ingredients - Common, easily accessible ingredients")
        self.luxurious_radio = QRadioButton("Luxurious Ingredients - Hard-to-find, premium ingredients")
        
        # Set default
        self.everyday_radio.setChecked(True)
        
        ingredient_layout.addWidget(self.everyday_radio)
        ingredient_layout.addWidget(self.luxurious_radio)
        
        # Seasonal ingredients checkbox
        self.seasonal_checkbox = QCheckBox("Prioritize seasonal ingredients")
        ingredient_layout.addWidget(self.seasonal_checkbox)
        
        ingredient_group.setLayout(ingredient_layout)
        layout.addWidget(ingredient_group)
        
        # Modern Gastronomy
        gastronomy_group = QGroupBox("Modern Gastronomy")
        gastronomy_layout = QVBoxLayout()
        
        # Slider for modern techniques
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Traditional"))
        
        self.gastronomy_slider = QSlider(Qt.Horizontal)
        self.gastronomy_slider.setRange(0, 100)
        self.gastronomy_slider.setValue(50)
        
        slider_layout.addWidget(self.gastronomy_slider)
        slider_layout.addWidget(QLabel("Molecular"))
        
        gastronomy_layout.addLayout(slider_layout)
        
        # Checkbox for specialized equipment
        self.specialized_equipment_checkbox = QCheckBox("Allow specialized equipment (sous vide, anti-griddle, etc.)")
        gastronomy_layout.addWidget(self.specialized_equipment_checkbox)
        
        gastronomy_group.setLayout(gastronomy_layout)
        layout.addWidget(gastronomy_group)
        
        # Add spacer
        layout.addStretch()
        
        return tab
    
    def create_dietary_occasion_tab(self):
        """Create the dietary restrictions and occasion tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Dietary Restrictions
        dietary_group = QGroupBox("Dietary Restrictions")
        dietary_layout = QVBoxLayout()
        
        # Checkboxes for dietary restrictions
        self.vegetarian_checkbox = QCheckBox("Vegetarian")
        self.vegan_checkbox = QCheckBox("Vegan")
        self.gluten_free_checkbox = QCheckBox("Gluten-Free")
        self.dairy_free_checkbox = QCheckBox("Dairy-Free")
        self.nut_free_checkbox = QCheckBox("Nut-Free")
        self.keto_checkbox = QCheckBox("Keto-Friendly")
        self.low_carb_checkbox = QCheckBox("Low-Carb")
        
        dietary_layout.addWidget(self.vegetarian_checkbox)
        dietary_layout.addWidget(self.vegan_checkbox)
        dietary_layout.addWidget(self.gluten_free_checkbox)
        dietary_layout.addWidget(self.dairy_free_checkbox)
        dietary_layout.addWidget(self.nut_free_checkbox)
        dietary_layout.addWidget(self.keto_checkbox)
        dietary_layout.addWidget(self.low_carb_checkbox)
        
        dietary_group.setLayout(dietary_layout)
        layout.addWidget(dietary_group)
        
        # Occasion
        occasion_group = QGroupBox("Occasion")
        occasion_layout = QVBoxLayout()
        
        # Dropdown for occasion
        occasion_layout.addWidget(QLabel("Select Occasion:"))
        self.occasion_combo = QComboBox()
        occasions = [
            "Everyday Meal",
            "Dinner Party",
            "Romantic Dinner",
            "Holiday Celebration",
            "Special Occasion",
            "Tasting Menu",
            "Family Gathering",
            "Brunch"
        ]
        self.occasion_combo.addItems(occasions)
        occasion_layout.addWidget(self.occasion_combo)
        
        # Number of servings
        servings_layout = QHBoxLayout()
        servings_layout.addWidget(QLabel("Number of Servings:"))
        self.servings_spin = QSpinBox()
        self.servings_spin.setRange(1, 12)
        self.servings_spin.setValue(4)
        servings_layout.addWidget(self.servings_spin)
        
        occasion_layout.addLayout(servings_layout)
        occasion_group.setLayout(occasion_layout)
        layout.addWidget(occasion_group)
        
        # Add spacer
        layout.addStretch()
        
        return tab
    
    def create_equipment_time_tab(self):
        """Create the equipment and time constraints tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Time Constraints
        time_group = QGroupBox("Time Constraints")
        time_layout = QVBoxLayout()
        
        # Slider for preparation time
        prep_layout = QHBoxLayout()
        prep_layout.addWidget(QLabel("Preparation Time:"))
        self.prep_time_slider = QSlider(Qt.Horizontal)
        self.prep_time_slider.setRange(15, 180)  # 15 minutes to 3 hours
        self.prep_time_slider.setValue(60)
        self.prep_time_label = QLabel("60 minutes")
        self.prep_time_slider.valueChanged.connect(lambda v: self.prep_time_label.setText(f"{v} minutes"))
        
        prep_layout.addWidget(self.prep_time_slider)
        prep_layout.addWidget(self.prep_time_label)
        time_layout.addLayout(prep_layout)
        
        # Slider for cooking time
        cook_layout = QHBoxLayout()
        cook_layout.addWidget(QLabel("Cooking Time:"))
        self.cook_time_slider = QSlider(Qt.Horizontal)
        self.cook_time_slider.setRange(15, 240)  # 15 minutes to 4 hours
        self.cook_time_slider.setValue(60)
        self.cook_time_label = QLabel("60 minutes")
        self.cook_time_slider.valueChanged.connect(lambda v: self.cook_time_label.setText(f"{v} minutes"))
        
        cook_layout.addWidget(self.cook_time_slider)
        cook_layout.addWidget(self.cook_time_label)
        time_layout.addLayout(cook_layout)
        
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # Equipment
        equipment_group = QGroupBox("Available Equipment")
        equipment_layout = QVBoxLayout()
        
        # Common equipment
        self.oven_checkbox = QCheckBox("Oven")
        self.stovetop_checkbox = QCheckBox("Stovetop")
        self.blender_checkbox = QCheckBox("Blender/Food Processor")
        self.mixer_checkbox = QCheckBox("Stand Mixer")
        self.sous_vide_checkbox = QCheckBox("Sous Vide")
        self.pressure_cooker_checkbox = QCheckBox("Pressure Cooker/Instant Pot")
        self.grill_checkbox = QCheckBox("Grill")
        self.smoker_checkbox = QCheckBox("Smoker")
        
        # Set defaults
        self.oven_checkbox.setChecked(True)
        self.stovetop_checkbox.setChecked(True)
        
        equipment_layout.addWidget(self.oven_checkbox)
        equipment_layout.addWidget(self.stovetop_checkbox)
        equipment_layout.addWidget(self.blender_checkbox)
        equipment_layout.addWidget(self.mixer_checkbox)
        equipment_layout.addWidget(self.sous_vide_checkbox)
        equipment_layout.addWidget(self.pressure_cooker_checkbox)
        equipment_layout.addWidget(self.grill_checkbox)
        equipment_layout.addWidget(self.smoker_checkbox)
        
        equipment_group.setLayout(equipment_layout)
        layout.addWidget(equipment_group)
        
        # Add spacer
        layout.addStretch()
        
        return tab
    
    def generate_recipe(self):
        """Generate a recipe based on the selected parameters"""
        # Collect all parameters
        params = self.collect_parameters()
        
        # Generate recipe
        try:
            recipe = self.recipe_generator.generate_recipe(params)
            self.display_recipe(recipe)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate recipe: {str(e)}")
    
    def collect_parameters(self):
        """Collect all parameters from the UI"""
        params = {
            "chefs": {},
            "michelin_stars": 1,
            "ingredient_type": "everyday",
            "seasonal": False,
            "gastronomy_level": 0,
            "specialized_equipment": False,
            "dietary_restrictions": [],
            "occasion": "",
            "servings": 4,
            "prep_time": 60,
            "cook_time": 60,
            "equipment": []
        }
        
        # Collect chef selections and influence
        for chef_id, checkbox in self.chef_checkboxes.items():
            if checkbox.isChecked():
                params["chefs"][chef_id] = self.chef_sliders[chef_id].value()
        
        # Michelin star rating
        if self.two_star_radio.isChecked():
            params["michelin_stars"] = 2
        elif self.three_star_radio.isChecked():
            params["michelin_stars"] = 3
        
        # Ingredient type
        if self.luxurious_radio.isChecked():
            params["ingredient_type"] = "luxurious"
        
        # Seasonal ingredients
        params["seasonal"] = self.seasonal_checkbox.isChecked()
        
        # Gastronomy level
        params["gastronomy_level"] = self.gastronomy_slider.value()
        params["specialized_equipment"] = self.specialized_equipment_checkbox.isChecked()
        
        # Dietary restrictions
        if self.vegetarian_checkbox.isChecked():
            params["dietary_restrictions"].append("vegetarian")
        if self.vegan_checkbox.isChecked():
            params["dietary_restrictions"].append("vegan")
        if self.gluten_free_checkbox.isChecked():
            params["dietary_restrictions"].append("gluten-free")
        if self.dairy_free_checkbox.isChecked():
            params["dietary_restrictions"].append("dairy-free")
        if self.nut_free_checkbox.isChecked():
            params["dietary_restrictions"].append("nut-free")
        if self.keto_checkbox.isChecked():
            params["dietary_restrictions"].append("keto")
        if self.low_carb_checkbox.isChecked():
            params["dietary_restrictions"].append("low-carb")
        
        # Occasion
        params["occasion"] = self.occasion_combo.currentText()
        params["servings"] = self.servings_spin.value()
        
        # Time constraints
        params["prep_time"] = self.prep_time_slider.value()
        params["cook_time"] = self.cook_time_slider.value()
        
        # Equipment
        if self.oven_checkbox.isChecked():
            params["equipment"].append("oven")
        if self.stovetop_checkbox.isChecked():
            params["equipment"].append("stovetop")
        if self.blender_checkbox.isChecked():
            params["equipment"].append("blender")
        if self.mixer_checkbox.isChecked():
            params["equipment"].append("mixer")
        if self.sous_vide_checkbox.isChecked():
            params["equipment"].append("sous_vide")
        if self.pressure_cooker_checkbox.isChecked():
            params["equipment"].append("pressure_cooker")
        if self.grill_checkbox.isChecked():
            params["equipment"].append("grill")
        if self.smoker_checkbox.isChecked():
            params["equipment"].append("smoker")
        
        return params
    
    def display_recipe(self, recipe):
        """Display the generated recipe in the recipe display"""
        self.recipe_display.setHtml(recipe["html_content"])
        self.current_recipe = recipe
    
    def save_recipe(self):
        """Save the current recipe to a file"""
        if not hasattr(self, 'current_recipe'):
            QMessageBox.warning(self, "Warning", "No recipe to save")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Recipe", "", "JSON Files (*.json);;HTML Files (*.html);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.html'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.current_recipe["html_content"])
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_recipe, f, indent=2)
            
            QMessageBox.information(self, "Success", f"Recipe saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save recipe: {str(e)}")
    
    def export_recipe(self):
        """Export the current recipe as PDF"""
        if not hasattr(self, 'current_recipe'):
            QMessageBox.warning(self, "Warning", "No recipe to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Recipe as PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # TODO: Implement PDF export functionality
            QMessageBox.information(self, "Not Implemented", "PDF export will be implemented in a future version")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export recipe: {str(e)}")
    
    def show_welcome_message(self):
        """Show welcome message in the recipe display"""
        welcome_html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                h2 { color: #555; }
                p { line-height: 1.5; }
            </style>
        </head>
        <body>
            <h1>Welcome to the Michelin Star Recipe Generator</h1>
            <p>Create custom recipes inspired by world-renowned Michelin-starred chefs.</p>
            <h2>How to use:</h2>
            <ol>
                <li>Select chefs and adjust their influence using the sliders</li>
                <li>Choose your desired Michelin star rating (1-3 stars)</li>
                <li>Select ingredient type (everyday or luxurious)</li>
                <li>Set dietary restrictions and occasion</li>
                <li>Adjust time constraints and available equipment</li>
                <li>Click "Generate Michelin Recipe" to create your custom recipe</li>
            </ol>
            <p>Your generated recipe will appear here with comprehensive instructions, chef notes, and technique tips.</p>
        </body>
        </html>
        """
        self.recipe_display.setHtml(welcome_html)


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    main_window = MichelinRecipeGenerator()
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()