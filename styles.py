# styles.py

"""
Zentrale Stylesheet-Definitionen für alle UI-Komponenten.
"""

from config import COLORS, BUTTONS, INPUTS, CHECKBOX, STATUS_LABEL

# Haupt-Stylesheet
STYLESHEET_MAIN_WINDOW = f"""
    QMainWindow {{
        background-color: {COLORS['dark']};
    }}
"""

# LineEdit (Text-Eingabefeld)
STYLESHEET_LINEEDIT = f"""
    QLineEdit {{
        background-color: {COLORS['dark_secondary']};
        border: {INPUTS['border_width']} solid {COLORS['border']};
        border-radius: {INPUTS['border_radius']};
        padding: {INPUTS['padding']};
        color: {COLORS['text']};
        font-size: {INPUTS['font_size']};
    }}
    QLineEdit:focus {{
        border: {INPUTS['border_width']} solid {COLORS['primary']};
        background-color: #323232;
    }}
    QLineEdit:hover {{
        background-color: #323232;
    }}
"""

# Primär-Button (JETZT NUR GRÜNE OUTLINE)
STYLESHEET_BUTTON_PRIMARY = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLORS['primary']};
        border: 2px solid {COLORS['primary']};
        border-radius: {BUTTONS['border_radius']};
        padding: {BUTTONS['primary_padding']};
        font-size: {BUTTONS['primary_font_size']};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary']}15;
        color: {COLORS['primary_hover']};
        border: 2px solid {COLORS['primary_hover']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary']}30;
        color: {COLORS['primary_pressed']};
        border: 2px solid {COLORS['primary_pressed']};
    }}
    QPushButton:disabled {{
        background-color: transparent;
        color: {COLORS['text_disabled']};
        border: 2px solid {COLORS['text_disabled']};
    }}
"""

# Sekundär-Button (OUTLINE DESIGN)
STYLESHEET_BUTTON_SECONDARY = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLORS['text']};
        border: 2px solid {COLORS['border']};
        border-radius: {BUTTONS['border_radius']};
        padding: {BUTTONS['secondary_padding']};
        font-size: {BUTTONS['secondary_font_size']};
    }}
    QPushButton:hover {{
        background-color: {COLORS['border']}20;
        color: {COLORS['text']};
        border: 2px solid {COLORS['text']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['border']}40;
        border: 2px solid {COLORS['text']};
    }}
    QPushButton:disabled {{
        background-color: transparent;
        color: {COLORS['text_disabled']};
        border: 2px solid {COLORS['text_disabled']};
    }}
"""

# Checkbox MIT GRÜNER CHECKMARK/PFEIL
STYLESHEET_CHECKBOX = f"""
    QCheckBox {{
        color: {COLORS['text']};
        font-size: {CHECKBOX['font_size']};
        spacing: {CHECKBOX['spacing']};
    }}
    QCheckBox::indicator {{
        width: {CHECKBOX['indicator_size']};
        height: {CHECKBOX['indicator_size']};
        border-radius: {CHECKBOX['indicator_radius']};
        border: 2px solid {COLORS['border']};
        background-color: {COLORS['dark_secondary']};
    }}
    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['primary']};
        background-color: {COLORS['dark_secondary']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLORS['dark_secondary']};
        border: 2px solid {COLORS['primary']};
        image: url(none);
    }}
"""

# Label (Standard)
STYLESHEET_LABEL = f"""
    QLabel {{
        color: {COLORS['text']};
    }}
"""

# Label (Untertitel/Beschreibung)
STYLESHEET_LABEL_DESCRIPTION = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 13px;
    }}
"""

# Label (Titel)
STYLESHEET_LABEL_TITLE = f"""
    QLabel {{
        color: {COLORS['primary']};
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }}
"""

# Status-Label
STYLESHEET_STATUS_LABEL = f"""
    QLabel {{
        background-color: transparent;
        padding: {STATUS_LABEL['padding']};
        border-radius: {STATUS_LABEL['border_radius']};
        font-size: {STATUS_LABEL['font_size']};
        font-weight: {STATUS_LABEL['font_weight']};
    }}
"""

# Frame (Optionen-Container)
STYLESHEET_FRAME_OPTIONS = f"""
    QFrame {{
        background-color: {COLORS['dark_secondary']};
        border-radius: 12px;
        padding: 15px;
    }}
"""

# Funktion zum Erstellen von Status-Label Styles
def get_status_label_style(success: bool) -> str:
    """
    Erstellt dynamisch ein Stylesheet für Status-Labels.
    
    Args:
        success (bool): True für erfolgreiche, False für Fehler-Meldungen
    
    Returns:
        str: Das Stylesheet
    """
    color = COLORS['success'] if success else COLORS['error']
    return f"""
        QLabel {{
            background-color: {color}20;
            color: {color};
            padding: {STATUS_LABEL['padding']};
            border-radius: {STATUS_LABEL['border_radius']};
            font-size: {STATUS_LABEL['font_size']};
            font-weight: {STATUS_LABEL['font_weight']};
            border: 2px solid {color};
        }}
    """