# ui/main_window.py

"""
Hauptfenster und Benutzeroberfläche für GitBackupTool Pro.
"""

import os
import platform
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    COLORS, MESSAGES, PLACEHOLDERS, LABELS, LAYOUTS, STATUS_LABEL
)
from styles import STYLESHEET_MAIN_WINDOW, STYLESHEET_FRAME_OPTIONS
from src.core import GitManager, FileManager, CloneWorker, Logger
from .widgets import (
    ModernLineEdit, ModernButton, ModernCheckBox,
    StatusLabel, DescriptionLabel, TitleLabel
)


class GitBackupToolPro(QMainWindow):
    """
    Hauptfenster der GitBackupTool Pro Anwendung.
    
    Verwaltet die Benutzeroberfläche und koordiniert die Interaktionen
    zwischen UI und der Backend-Logik.
    """
    
    def __init__(self):
        """Initialisiert das Hauptfenster."""
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Manager-Instanzen
        self.logger = Logger()
        self.git_manager = GitManager(self.logger)
        self.file_manager = FileManager(self.logger)
        
        # Worker-Thread (wird später initialisiert)
        self.worker: Optional[CloneWorker] = None
        
        # UI aufbauen
        self._setup_ui()
        self._load_last_used_repo()
        self._center_window()
        
        self.logger.info("Application started")
    
    def _setup_ui(self) -> None:
        """Initialisiert die komplette Benutzeroberfläche."""
        # Main Stylesheet
        self.setStyleSheet(STYLESHEET_MAIN_WINDOW)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(
            LAYOUTS['margin'],
            LAYOUTS['margin'],
            LAYOUTS['margin'],
            LAYOUTS['margin']
        )
        main_layout.setSpacing(LAYOUTS['spacing'])
        
        # Titel
        title = TitleLabel(LABELS['title'])
        main_layout.addWidget(title)
        
        # Status Label
        self.status_label = StatusLabel()
        main_layout.addWidget(self.status_label)
        
        # GitHub URL Input
        main_layout.addLayout(self._create_github_url_section())
        
        # Folder Name Input
        main_layout.addLayout(self._create_folder_name_section())
        
        # Save Path Input
        main_layout.addLayout(self._create_save_path_section())
        
        # Options Frame
        main_layout.addWidget(self._create_options_frame())
        
        # Spacer
        main_layout.addStretch()
        
        # Buttons
        main_layout.addLayout(self._create_button_section())
    
    def _create_github_url_section(self) -> QVBoxLayout:
        """
        Erstellt den Input-Bereich für die GitHub-URL.
        
        Returns:
            QVBoxLayout: Das Layout mit GitHub-URL Input
        """
        layout = QVBoxLayout()
        layout.setSpacing(LAYOUTS['label_spacing'])
        
        label = DescriptionLabel(LABELS['github_url'])
        self.github_url_entry = ModernLineEdit(PLACEHOLDERS['github_url'])
        
        layout.addWidget(label)
        layout.addWidget(self.github_url_entry)
        
        return layout
    
    def _create_folder_name_section(self) -> QVBoxLayout:
        """
        Erstellt den Input-Bereich für den lokalen Ordnernamen.
        
        Returns:
            QVBoxLayout: Das Layout mit Folder-Name Input
        """
        layout = QVBoxLayout()
        layout.setSpacing(LAYOUTS['label_spacing'])
        
        label = DescriptionLabel(LABELS['folder_name'])
        self.folder_name_entry = ModernLineEdit(PLACEHOLDERS['folder_name'])
        
        layout.addWidget(label)
        layout.addWidget(self.folder_name_entry)
        
        return layout
    
    def _create_save_path_section(self) -> QVBoxLayout:
        """
        Erstellt den Input-Bereich für den Speicherpfad mit Browse-Button.
        
        Returns:
            QVBoxLayout: Das Layout mit Save-Path Input und Browse-Button
        """
        layout = QVBoxLayout()
        layout.setSpacing(LAYOUTS['label_spacing'])
        
        label = DescriptionLabel(LABELS['save_location'])
        
        # Horizontal Layout für Input und Button
        path_input_layout = QHBoxLayout()
        path_input_layout.setSpacing(LAYOUTS['input_spacing'])
        
        self.path_entry = ModernLineEdit(PLACEHOLDERS['save_location'])
        browse_button = ModernButton(LABELS['browse_button'])
        browse_button.clicked.connect(self._browse_folder)
        browse_button.setFixedWidth(120)
        
        path_input_layout.addWidget(self.path_entry)
        path_input_layout.addWidget(browse_button)
        
        layout.addWidget(label)
        layout.addLayout(path_input_layout)
        
        return layout
    
    def _create_options_frame(self) -> QFrame:
        """
        Erstellt den Options-Frame mit Checkboxes.
        
        Returns:
            QFrame: Das Options-Frame mit Checkboxes
        """
        frame = QFrame()
        frame.setStyleSheet(STYLESHEET_FRAME_OPTIONS)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(LAYOUTS['input_spacing'])
        
        self.backup_checkbox = ModernCheckBox(LABELS['backup_option'])
        self.zip_checkbox = ModernCheckBox(LABELS['zip_option'])
        
        layout.addWidget(self.backup_checkbox)
        layout.addWidget(self.zip_checkbox)
        
        return frame
    
    def _create_button_section(self) -> QHBoxLayout:
        """
        Erstellt die Button-Sektion mit Clone, Clear und Log Buttons.
        
        Returns:
            QHBoxLayout: Das Layout mit allen Action-Buttons
        """
        layout = QHBoxLayout()
        layout.setSpacing(LAYOUTS['button_spacing'])
        
        # Clone Button (Primary)
        self.clone_button = ModernButton(LABELS['clone_button'], primary=True)
        self.clone_button.clicked.connect(self._clone_repo)
        
        # Clear Button
        clear_button = ModernButton(LABELS['clear_button'])
        clear_button.clicked.connect(self._clear_entries)
        
        # Log Button
        log_button = ModernButton(LABELS['log_button'])
        log_button.clicked.connect(self._open_log)
        
        layout.addWidget(self.clone_button, stretch=2)
        layout.addWidget(clear_button, stretch=1)
        layout.addWidget(log_button, stretch=1)
        
        return layout
    
    def _center_window(self) -> None:
        """Zentriert das Fenster auf dem Bildschirm."""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def _browse_folder(self) -> None:
        """Öffnet einen Folder-Selection-Dialog."""
        folder = QFileDialog.getExistingDirectory(self, LABELS['save_location'])
        if folder:
            self.path_entry.setText(folder)
            self.logger.debug(f"Folder selected: {folder}")
    
    def _clone_repo(self) -> None:
        """Startet den Repository-Clone-Prozess nach Validierung."""
        # Input-Daten sammeln
        github_url = self.github_url_entry.text().strip()
        folder_name = self.folder_name_entry.text().strip()
        target_path = self.path_entry.text().strip()
        
        # Validierung: Alle Felder gefüllt?
        if not github_url or not folder_name or not target_path:
            self.status_label.show_message(
                MESSAGES['fill_fields'],
                success=False,
                auto_hide_ms=STATUS_LABEL['auto_hide_ms']
            )
            self.logger.warning("Clone attempt with empty fields")
            return
        
        # Validierung: GitHub URL gültig?
        if not self.git_manager.is_valid_url(github_url):
            self.status_label.show_message(
                MESSAGES['invalid_url'],
                success=False,
                auto_hide_ms=STATUS_LABEL['auto_hide_ms']
            )
            return
        
        # UI für Clone-Operation deaktivieren
        self.clone_button.setEnabled(False)
        self.clone_button.setText(MESSAGES['clone_in_progress'])
        
        # Worker Thread erstellen und starten
        self.worker = CloneWorker(
            github_url,
            folder_name,
            target_path,
            add_backup=self.backup_checkbox.isChecked(),
            create_zip=self.zip_checkbox.isChecked()
        )
        self.worker.finished.connect(self._on_clone_finished)
        self.worker.progress.connect(self._on_clone_progress)
        self.worker.start()
        
        self.logger.info(f"Clone started: {github_url}")
    
    def _on_clone_progress(self, message: str) -> None:
        """
        Callback für Fortschritts-Updates während des Clone.
        
        Args:
            message (str): Die Fortschritts-Nachricht
        """
        self.status_label.show_message(message, success=True)
    
    def _on_clone_finished(self, success: bool, message: str) -> None:
        """
        Callback wenn Clone-Operation fertig ist.
        
        Args:
            success (bool): True wenn erfolgreich, False bei Fehler
            message (str): Status-Nachricht
        """
        # UI reaktivieren
        self.clone_button.setEnabled(True)
        self.clone_button.setText(LABELS['clone_button'])
        
        # Status anzeigen
        self.status_label.show_message(
            message,
            success=success,
            auto_hide_ms=STATUS_LABEL['auto_hide_ms']
        )
        
        # Wenn erfolgreich, Konfiguration speichern
        if success:
            self._save_last_used_repo(github_url=self.github_url_entry.text(), path=self.path_entry.text())
    
    def _clear_entries(self) -> None:
        """Löscht alle Input-Felder und versteckt Status-Label."""
        self.github_url_entry.clear()
        self.folder_name_entry.clear()
        self.path_entry.clear()
        self.backup_checkbox.setChecked(False)
        self.zip_checkbox.setChecked(False)
        self.status_label.hide_message()
        self.logger.debug("All entries cleared")
    
    def _save_last_used_repo(self, github_url: str, path: str) -> None:
        """
        Speichert die zuletzt verwendete Repository-Info.
        
        Args:
            github_url (str): Die GitHub-URL
            path (str): Der Speicherpfad
        """
        data = {
            "github_url": github_url,
            "path": path
        }
        success, msg = self.file_manager.save_config(data)
        if success:
            self.logger.debug("Last used repo saved")
    
    def _load_last_used_repo(self) -> None:
        """Lädt die zuletzt verwendete Repository-Info."""
        data = self.file_manager.load_config()
        if data:
            self.github_url_entry.setText(data.get("github_url", ""))
            self.path_entry.setText(data.get("path", ""))
            self.logger.debug("Last used repo loaded")
    
    def _open_log(self) -> None:
        """Öffnet die Log-Datei im Standard-Editor des Betriebssystems."""
        log_file = self.logger.get_log_file_path()
        
        if not os.path.exists(log_file):
            self.status_label.show_message(
                MESSAGES['log_not_found'],
                success=False,
                auto_hide_ms=STATUS_LABEL['auto_hide_ms']
            )
            return
        
        try:
            if platform.system() == "Windows":
                os.system(f"notepad {log_file}")
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open {log_file}")
            else:  # Linux
                os.system(f"xdg-open {log_file}")
            self.logger.info("Log file opened")
        except Exception as e:
            self.logger.error(f"Error opening log file: {str(e)}")
            self.status_label.show_message(
                f"Error opening log file: {str(e)}",
                success=False,
                auto_hide_ms=STATUS_LABEL['auto_hide_ms']
            )