from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt

class ApiKeyDialog(QDialog):
    """Dialog for setting up the OpenAI API key"""
    
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.api_key = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("OpenAI API Key Setup")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Add explanation
        explanation = QLabel(
            "This application requires an OpenAI API key to generate recipes. "
            "Your API key will be stored securely using your system's keyring."
        )
        explanation.setWordWrap(True)
        layout.addWidget(explanation)
        
        # Add instructions
        instructions = QLabel(
            "To obtain an API key:\n"
            "1. Create an account at https://openai.com/\n"
            "2. Navigate to the API section\n"
            "3. Generate a new API key\n"
            "4. Enter the key below"
        )
        layout.addWidget(instructions)
        
        # Add API key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API Key:"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)
        
        # Add buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save API Key")
        cancel_button = QPushButton("Cancel")
        
        save_button.clicked.connect(self.save_api_key)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_api_key(self):
        """Save the API key and close the dialog"""
        api_key = self.key_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key")
            return
        
        # Save the API key
        success = self.settings_manager.save_api_key(api_key)
        
        if success:
            self.api_key = api_key
            self.accept()
        else:
            QMessageBox.critical(
                self, "Error", 
                "Failed to save API key. Please check your system's keyring configuration."
            )