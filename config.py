# config.py

"""
Zentrale Konfigurationsdatei für GitBackupTool Pro.
Alle Konstanten, Farben und Nachrichten sind hier definiert.
"""

# Fenster-Einstellungen
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 550
WINDOW_TITLE = "GitBackupTool Pro"
WINDOW_MIN_WIDTH = 750
WINDOW_MIN_HEIGHT = 600

# Datei-Einstellungen
LOG_FILE = "log.txt"
CONFIG_FILE = "last_used_repo.json"

# Git-Einstellungen
GIT_CLONE_TIMEOUT = 10

# Farben (Dark Theme)
COLORS = {
    "primary": "#4CAF50",
    "primary_hover": "#45a049",
    "primary_pressed": "#3d8b40",
    "dark": "#1e1e1e",
    "dark_secondary": "#2b2b2b",
    "border": "#3d3d3d",
    "text": "#ffffff",
    "text_secondary": "#b0b0b0",
    "text_disabled": "#666666",
    "error": "#f44336",
    "success": "#4CAF50",
    "button_bg": "#3d3d3d",
    "button_hover": "#4d4d4d",
    "button_pressed": "#2d2d2d",
}

# UI-Texte und Nachrichten
MESSAGES = {
    "success": "Repository successfully cloned!",
    "invalid_url": "Invalid or unreachable GitHub URL",
    "fill_fields": "Please fill in all fields",
    "clone_in_progress": "Cloning...",
    "clone_complete": "Clone Repository",
    "log_not_found": "Log file not found",
    "error_prefix": "Error: ",
    "unexpected_error": "Unexpected error: ",
}

# Platzhalter-Texte
PLACEHOLDERS = {
    "github_url": "https://github.com/username/repository",
    "folder_name": "my-project",
    "save_location": "/path/to/save",
}

# Labels
LABELS = {
    "title": "GitBackupTool Pro",
    "github_url": "GitHub Repository URL",
    "folder_name": "Local Folder Name",
    "save_location": "Save Location",
    "backup_option": "Create timestamped backup folder",
    "zip_option": "Create ZIP archive after cloning",
    "clone_button": "Clone Repository",
    "clear_button": "Clear All",
    "log_button": "View Log",
    "browse_button": "Browse",
}

# Layout-Einstellungen
LAYOUTS = {
    "margin": 30,
    "spacing": 20,
    "label_spacing": 8,
    "button_spacing": 15,
    "input_spacing": 10,
}

# Button-Einstellungen
BUTTONS = {
    "primary_padding": "12px 24px",
    "primary_font_size": "14px",
    "secondary_padding": "12px 24px",
    "secondary_font_size": "14px",
    "border_radius": "8px",
}

# Input-Einstellungen
INPUTS = {
    "padding": "10px 15px",
    "border_radius": "8px",
    "font_size": "14px",
    "border_width": "2px",
}

# Status-Label Einstellungen
STATUS_LABEL = {
    "auto_hide_ms": 3000,
    "padding": "10px",
    "border_radius": "8px",
    "font_size": "14px",
    "font_weight": "bold",
}

# Checkbox-Einstellungen
CHECKBOX = {
    "indicator_size": "20px",
    "indicator_radius": "5px",
    "font_size": "14px",
    "spacing": "8px",
}