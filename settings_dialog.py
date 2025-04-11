# michelin_recipe_generator/settings_dialog.py
import sys
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QDialogButtonBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

# Assuming SettingsManager is in the same directory or accessible via path
from .settings_manager import SettingsManager 

class SettingsDialog(QDialog):
    """
    A dialog window for configuring application settings, specifically the OpenAI model.
    """
    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.available_models = ["gpt-4", "gpt-4o"] # Removed o1 model

        self.setWindowTitle("Settings")
        self.setMinimumWidth(350)

        # --- UI Elements ---
        self.model_label = QLabel("Select OpenAI Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.available_models)

        # --- Layout ---
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.model_label)
        form_layout.addWidget(self.model_combo)
        form_layout.addStretch() # Push elements to the left

        # --- Buttons ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept_settings)
        self.button_box.rejected.connect(self.reject)

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)) # Spacer
        main_layout.addWidget(self.button_box)

        # --- Load Initial Settings ---
        self._load_initial_settings()

    def _load_initial_settings(self):
        """Load current settings and populate the UI elements."""
        current_model = self.settings_manager.get_setting('api_settings.model', 'gpt-4') # Default fallback
        
        if current_model in self.available_models:
            index = self.model_combo.findText(current_model, Qt.MatchFixedString)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
        else:
            # Handle case where saved model is not in the current list (optional)
            # Maybe add it temporarily or default to the first item
            print(f"Warning: Saved model '{current_model}' not in available list. Defaulting.")
            self.model_combo.setCurrentIndex(0)


    def accept_settings(self):
        """Save the selected settings and close the dialog."""
        selected_model = self.model_combo.currentText()
        self.settings_manager.set_setting('api_settings.model', selected_model)
        self.accept() # Close dialog with QDialog.Accepted status

# Example usage (for testing purposes)
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    # Need a dummy SettingsManager for testing
    class DummySettingsManager:
        def __init__(self):
            self._settings = {'api_settings': {'model': 'gpt-4o'}}
        def get_setting(self, key, default=None):
            keys = key.split('.')
            val = self._settings
            try:
                for k in keys: val = val[k]
                return val
            except KeyError: return default
        def set_setting(self, key, value):
            keys = key.split('.')
            d = self._settings
            for k in keys[:-1]: d = d.setdefault(k, {})
            d[keys[-1]] = value
            print(f"Set {key} to {value}")
            print(f"Current settings: {self._settings}")

    app = QApplication(sys.argv)
    dummy_manager = DummySettingsManager()
    dialog = SettingsDialog(dummy_manager)
    
    # Apply dark theme if available (assuming dark_theme.qss exists)
    try:
        with open("styles/dark_theme.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Dark theme stylesheet not found, using default.")

    if dialog.exec_() == QDialog.Accepted:
        print("Settings saved.")
    else:
        print("Settings cancelled.")
    
    sys.exit()