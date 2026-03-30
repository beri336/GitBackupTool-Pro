# core/logger.py

"""
Zentrales Logging-System für GitBackupTool Pro.
Verwaltet alle Log-Operationen in einer einzigen Stelle.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional
from config import LOG_FILE


class Logger:
    """
    Zentrale Logger-Klasse für alle Logging-Operationen.
    
    Attributes:
        log_file (str): Pfad zur Log-Datei
    """
    
    def __init__(self, log_file: str = LOG_FILE) -> None:
        """
        Initialisiert den Logger.
        
        Args:
            log_file (str): Name oder Pfad der Log-Datei. Default aus config.py
        """
        self.log_file = log_file
        self._ensure_log_file_exists()
    
    def _ensure_log_file_exists(self) -> None:
        """Stellt sicher, dass die Log-Datei existiert."""
        try:
            Path(self.log_file).touch(exist_ok=True)
        except Exception as e:
            print(f"Fehler beim Erstellen der Log-Datei: {e}")
    
    def _write_log(self, message: str) -> None:
        """
        Schreibt eine Nachricht in die Log-Datei.
        
        Args:
            message (str): Die zu loggenden Nachricht
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
        except IOError as e:
            print(f"Fehler beim Schreiben der Log-Datei: {e}")
    
    def info(self, message: str) -> None:
        """
        Loggt eine Info-Nachricht.
        
        Args:
            message (str): Die Info-Nachricht
        """
        self._write_log(f"[INFO] {message}")
    
    def success(self, message: str) -> None:
        """
        Loggt eine Erfolgs-Nachricht.
        
        Args:
            message (str): Die Erfolgs-Nachricht
        """
        self._write_log(f"[SUCCESS] {message}")
    
    def warning(self, message: str) -> None:
        """
        Loggt eine Warn-Nachricht.
        
        Args:
            message (str): Die Warn-Nachricht
        """
        self._write_log(f"[WARNING] {message}")
    
    def error(self, message: str) -> None:
        """
        Loggt eine Fehler-Nachricht.
        
        Args:
            message (str): Die Fehler-Nachricht
        """
        self._write_log(f"[ERROR] {message}")
    
    def debug(self, message: str) -> None:
        """
        Loggt eine Debug-Nachricht.
        
        Args:
            message (str): Die Debug-Nachricht
        """
        self._write_log(f"[DEBUG] {message}")
    
    def get_log_file_path(self) -> str:
        """
        Gibt den Pfad zur Log-Datei zurück.
        
        Returns:
            str: Der Pfad zur Log-Datei
        """
        return self.log_file
    
    def clear_log(self) -> None:
        """Löscht alle Log-Einträge."""
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")
            self.info("Log file cleared")
        except IOError as e:
            print(f"Fehler beim Löschen der Log-Datei: {e}")