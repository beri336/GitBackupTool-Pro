# main.py

"""
GitBackupTool Pro - Haupteinstiegspunkt
Ein einfaches GUI-Tool zum Klonen von GitHub-Repositories, Erstellen von Backups und Generieren von ZIP-Archiven.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from config import COLORS
from src.ui import GitBackupToolPro


def setup_dark_palette(app: QApplication) -> None:
    """
    Setzt ein globales Dark-Theme-Palette für die Anwendung.
    
    Args:
        app (QApplication): Die QApplication-Instanz
    """
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(COLORS['dark']))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(COLORS['dark_secondary']))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(COLORS['primary']))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    app.setPalette(palette)


def main() -> None:
    """Haupteinstiegspunkt der Anwendung."""
    # QApplication erstellen
    app = QApplication(sys.argv)
    
    # Fusion-Style setzen (Cross-Platform)
    app.setStyle("Fusion")
    
    # Dark-Palette anwenden
    setup_dark_palette(app)
    
    # Hauptfenster erstellen und anzeigen
    window = GitBackupToolPro()
    window.show()
    
    # Event-Loop starten
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
