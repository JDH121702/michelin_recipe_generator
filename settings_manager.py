import os
import json
import keyring
from pathlib import Path

class SettingsManager:
    """
    Manages application settings and API keys for the Michelin Star Recipe Generator.
    Handles secure storage and retrieval of API keys using the keyring library.
    """
    
    def __init__(self):
        """Initialize the settings manager"""
        # Define app name for keyring
        self.app_name = "MichelinRecipeGenerator"
        self.api_key_name = "openai_api_key"
        
        # Create app directory if it doesn't exist
        self.app_dir = self._get_app_directory()
        self.app_dir.mkdir(parents=True, exist_ok=True)
        
        # Settings file path
        self.settings_file = self.app_dir / "settings.json"
        
        # Load or create settings
        self.settings = self._load_settings()
    
    def _get_app_directory(self):
        """Get the application directory based on the operating system"""
        home = Path.home()
        
        if os.name == 'nt':  # Windows
            app_dir = home / "AppData" / "Local" / "MichelinRecipeGenerator"
        elif os.name == 'posix':  # macOS/Linux
            app_dir = home / ".config" / "michelin_recipe_generator"
        else:
            app_dir = home / ".michelin_recipe_generator"
        
        return app_dir
    
    def _load_settings(self):
        """Load settings from file or create default settings"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, create new settings
                return self._create_default_settings()
        else:
            return self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings"""
        default_settings = {
            "theme": "dark",
            "save_recipes": True,
            "recipe_history_size": 10,
            "default_servings": 4,
            "api_settings": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "has_api_key": False
        }
        
        # Save default settings
        self._save_settings(default_settings)
        return default_settings
    
    def _save_settings(self, settings=None):
        """Save settings to file"""
        if settings is None:
            settings = self.settings
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def get_setting(self, key, default=None):
        """Get a setting value by key"""
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key, value):
        """Set a setting value by key"""
        keys = key.split('.')
        settings = self.settings
        
        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        # Set the value
        settings[keys[-1]] = value
        
        # Save settings
        self._save_settings()
    
    def save_api_key(self, api_key):
        """Save the OpenAI API key securely"""
        if not api_key:
            return False
        
        try:
            # Store API key in the system's secure storage
            keyring.set_password(self.app_name, self.api_key_name, api_key)
            
            # Update settings to indicate API key is set
            self.settings["has_api_key"] = True
            self._save_settings()
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False
    
    def get_api_key(self):
        """Get the OpenAI API key from secure storage"""
        if not self.settings.get("has_api_key", False):
            return None
        
        try:
            return keyring.get_password(self.app_name, self.api_key_name)
        except Exception as e:
            print(f"Error retrieving API key: {e}")
            return None
    
    def delete_api_key(self):
        """Delete the stored API key"""
        try:
            keyring.delete_password(self.app_name, self.api_key_name)
            self.settings["has_api_key"] = False
            self._save_settings()
            return True
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False
    
    def has_api_key(self):
        """Check if an API key is stored"""
        return self.settings.get("has_api_key", False)
    
    def get_recipe_history_file(self):
        """Get the path to the recipe history file"""
        return self.app_dir / "recipe_history.json"
    
    def save_recipe_to_history(self, recipe):
        """Save a generated recipe to history"""
        if not self.get_setting("save_recipes", True):
            return
        
        history_file = self.get_recipe_history_file()
        history = []
        
        # Load existing history if available
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []
        
        # Add new recipe to history
        history.append({
            "title": recipe.get("title", "Untitled Recipe"),
            "timestamp": recipe.get("timestamp"),
            "recipe": recipe
        })
        
        # Limit history size
        max_size = self.get_setting("recipe_history_size", 10)
        if len(history) > max_size:
            history = history[-max_size:]
        
        # Save history
        try:
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except IOError as e:
            print(f"Error saving recipe history: {e}")
    
    def get_recipe_history(self):
        """Get the recipe history"""
        history_file = self.get_recipe_history_file()
        
        if not history_file.exists():
            return []
        
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def clear_recipe_history(self):
        """Clear the recipe history"""
        history_file = self.get_recipe_history_file()
        
        if history_file.exists():
            try:
                os.remove(history_file)
                return True
            except IOError:
                return False
        
        return True