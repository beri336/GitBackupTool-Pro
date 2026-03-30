# ui/widgets.py

"""
Custom UI-Widgets mit moderner Gestaltung.
"""

from typing import Optional
from PySide6.QtWidgets import QLineEdit, QPushButton, QCheckBox, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
from styles import (
    STYLESHEET_LINEEDIT,
    STYLESHEET_BUTTON_PRIMARY,
    STYLESHEET_BUTTON_SECONDARY,
    STYLESHEET_CHECKBOX,
    STYLESHEET_LABEL_DESCRIPTION,
    STYLESHEET_LABEL_TITLE,
    STYLESHEET_STATUS_LABEL,
    get_status_label_style
)
from config import COLORS


class ModernLineEdit(QLineEdit):
    """
    Custom LineEdit mit modernem Styling.
    Verwendet zentrale Stylesheets aus styles.py.
    """
    
    def __init__(self, placeholder: str = "", parent=None):
        """
        Initialisiert das ModernLineEdit.
        
        Args:
            placeholder (str): Platzhalter-Text
            parent: Parent-Widget
        """
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(STYLESHEET_LINEEDIT)


class ModernButton(QPushButton):
    """
    Custom Button mit modernem Styling - OUTLINE DESIGN.
    Grüner Rahmen mit transparentem Hintergrund für Primary-Buttons.
    """
    
    def __init__(self, text: str, primary: bool = False, parent=None):
        """
        Initialisiert den ModernButton.
        
        Args:
            text (str): Beschriftung des Buttons
            primary (bool): True für Aktions-Button, False für Normal-Button
            parent: Parent-Widget
        """
        super().__init__(text, parent)
        self.is_primary = primary
        self._apply_style()
    
    def _apply_style(self) -> None:
        """Wendet das entsprechende Stylesheet an."""
        if self.is_primary:
            self.setStyleSheet(STYLESHEET_BUTTON_PRIMARY)
        else:
            self.setStyleSheet(STYLESHEET_BUTTON_SECONDARY)
    
    def set_primary(self, primary: bool) -> None:
        """
        Wechselt zwischen primärem und sekundärem Style.
        
        Args:
            primary (bool): True für primär, False für sekundär
        """
        self.is_primary = primary
        self._apply_style()


class ModernCheckBox(QCheckBox):
    """
    Custom CheckBox mit modernem Styling und ZENTRIERTEM grünem Häkchen.
    """
    
    def __init__(self, text: str, parent=None):
        """
        Initialisiert die ModernCheckBox.
        
        Args:
            text (str): Label des Checkboxes
            parent: Parent-Widget
        """
        super().__init__(text, parent)
        self.setStyleSheet(STYLESHEET_CHECKBOX)
        self.stateChanged.connect(self._on_state_changed)
    
    def _on_state_changed(self):
        """Wird aufgerufen wenn der State sich ändert."""
        self.update()  # Widget neu zeichnen
    
    def paintEvent(self, event):
        """Custom painting für zentriertes grünes Häkchen."""
        super().paintEvent(event)
        
        # Nur wenn gecheckt
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Checkbox-Box Größe und Position (Standard: 20x20)
            indicator_size = 20
            margin = 4
            box_x = margin
            box_y = (self.height() - indicator_size) // 2
            
            # Häkchen-Farbe (Grün)
            check_color = QColor(COLORS['primary'])
            
            # Pen für das Häkchen (dickere Linie)
            pen = QPen(check_color, 2.5)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            # Häkchen-Position ZENTRIERT IN DER BOX
            # Kleine Linie (unten-links nach Mitte)
            check_start_x = box_x + indicator_size * 0.3
            check_start_y = box_y + indicator_size * 0.55
            check_middle_x = box_x + indicator_size * 0.45
            check_middle_y = box_y + indicator_size * 0.70
            
            # Große Linie (Mitte nach oben-rechts)
            check_end_x = box_x + indicator_size * 0.75
            check_end_y = box_y + indicator_size * 0.30
            
            # Häkchen zeichnen (zwei Linien)
            painter.drawLine(
                int(check_start_x), int(check_start_y),
                int(check_middle_x), int(check_middle_y)
            )
            painter.drawLine(
                int(check_middle_x), int(check_middle_y),
                int(check_end_x), int(check_end_y)
            )
            
            painter.end()


class DescriptionLabel(QLabel):
    """
    Label für Beschreibungs- und Untertitel-Text.
    Verwendet sekundäre Textfarbe und kleinere Schriftgröße.
    """
    
    def __init__(self, text: str = "", parent=None):
        """
        Initialisiert das DescriptionLabel.
        
        Args:
            text (str): Der Label-Text
            parent: Parent-Widget
        """
        super().__init__(text, parent)
        self.setStyleSheet(STYLESHEET_LABEL_DESCRIPTION)


class TitleLabel(QLabel):
    """
    Label für Titel-Text.
    Verwendet primäre Farbe und größere Schriftgröße.
    """
    
    def __init__(self, text: str = "", parent=None):
        """
        Initialisiert das TitleLabel.
        
        Args:
            text (str): Der Titel-Text
            parent: Parent-Widget
        """
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(STYLESHEET_LABEL_TITLE)


class StatusLabel(QLabel):
    """
    Animiertes Status-Label für Benutzer-Feedback.
    Zeigt Erfolgs- oder Fehler-Meldungen mit farblicher Codierung.
    """
    
    def __init__(self, parent=None):
        """
        Initialisiert das StatusLabel.
        
        Args:
            parent: Parent-Widget
        """
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(STYLESHEET_STATUS_LABEL)
        self.hide()
        self._auto_hide_timer = QTimer()
        self._auto_hide_timer.timeout.connect(self.hide)
    
    def show_message(self, message: str, success: bool = True, auto_hide_ms: int = 3000) -> None:
        """
        Zeigt eine Status-Nachricht an.
        
        Args:
            message (str): Die anzuzeigende Nachricht
            success (bool): True für Erfolgs-, False für Fehler-Nachricht
            auto_hide_ms (int): Millisekunden bis zur automatischen Ausblendung
        """
        # Dynamisches Stylesheet basierend auf Erfolg/Fehler
        self.setStyleSheet(get_status_label_style(success))
        self.setText(message)
        self.show()
        
        # Auto-hide Timer starten
        self._auto_hide_timer.stop()
        self._auto_hide_timer.start(auto_hide_ms)
    
    def hide_message(self) -> None:
        """Versteckt die Nachricht sofort und stoppt den Timer."""
        self._auto_hide_timer.stop()
        self.hide()