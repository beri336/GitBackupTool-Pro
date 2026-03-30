# core/worker.py

"""
Worker-Thread für die Clone-Operation ohne UI-Blockierung.
"""

import os
from typing import Callable
from PySide6.QtCore import QThread, Signal
from .logger import Logger
from .git_manager import GitManager
from .file_manager import FileManager


class CloneWorker(QThread):
    """
    Worker-Thread für Repository-Clone-Operationen.
    Verhindert, dass die UI blockiert wird während Git klont.
    
    Signals:
        finished: Signal(bool, str) - Emittiert wenn Clone fertig ist
        progress: Signal(str) - Emittiert Fortschritts-Nachrichten
    """
    
    # Signals definieren
    finished = Signal(bool, str)  # (success, message)
    progress = Signal(str)
    
    def __init__(
        self,
        github_url: str,
        folder_name: str,
        target_path: str,
        add_backup: bool = False,
        create_zip: bool = False
    ) -> None:
        """
        Initialisiert den CloneWorker.
        
        Args:
            github_url (str): Die GitHub-URL des zu klonenden Repositories
            folder_name (str): Der Name des lokalen Ordners
            target_path (str): Der Pfad wo das Repository gespeichert wird
            add_backup (bool): Ob ein Zeitstempel-Backup erstellt wird
            create_zip (bool): Ob nach dem Clone ein ZIP erstellt wird
        """
        super().__init__()
        self.github_url = github_url
        self.folder_name = folder_name
        self.target_path = target_path
        self.add_backup = add_backup
        self.create_zip = create_zip
        
        # Manager-Instanzen
        self.logger = Logger()
        self.git_manager = GitManager(self.logger)
        self.file_manager = FileManager(self.logger)
    
    def run(self) -> None:
        """
        Führt die Clone-Operation aus.
        Diese Methode wird in einem separaten Thread ausgeführt.
        """
        try:
            # Schritt 1: Backup-Ordnernamen generieren
            self.progress.emit("Preparing backup folder...")
            backup_folder_name = self.file_manager.create_backup_folder_name(
                self.folder_name,
                add_timestamp=self.add_backup
            )
            target_directory = os.path.join(self.target_path, backup_folder_name)
            
            # Schritt 2: Verzeichnis erstellen
            self.progress.emit("Creating directory...")
            success, msg = self.file_manager.ensure_directory_exists(target_directory)
            if not success:
                self.finished.emit(False, msg)
                return
            
            # Schritt 3: Repository klonen
            self.progress.emit("Cloning repository...")
            success, clone_msg = self.git_manager.clone(self.github_url, target_directory)
            if not success:
                self.finished.emit(False, clone_msg)
                return
            
            # Schritt 4: ZIP-Archiv erstellen wenn gewünscht
            if self.create_zip:
                self.progress.emit("Creating ZIP archive...")
                success, zip_msg = self.file_manager.create_zip_archive(target_directory)
                if not success:
                    self.logger.warning(f"ZIP creation failed: {zip_msg}")
                    # Aber nicht abbrechen, Clone war erfolgreich
            
            # Erfolg
            success_msg = f"Repository successfully cloned to {target_directory}"
            self.logger.success(success_msg)
            self.finished.emit(True, success_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            self.finished.emit(False, error_msg)