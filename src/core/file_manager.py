# core/file_manager.py

"""
Datei-Manager für alle Datei-Operationen.
Verwaltet ZIP-Archive, Konfigurationsdateien und Backups.
"""

import os
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from config import CONFIG_FILE
from .logger import Logger


class FileManager:
    """
    Manager für alle Datei-Operationen.
    
    Attributes:
        logger (Logger): Logger-Instanz für Logging
        config_file (str): Pfad zur Konfigurationsdatei
    """
    
    def __init__(self, logger: Logger = None, config_file: str = CONFIG_FILE) -> None:
        """
        Initialisiert den FileManager.
        
        Args:
            logger (Logger): Logger-Instanz. Wenn None, wird eine neue erstellt
            config_file (str): Pfad zur Konfigurationsdatei. Default aus config.py
        """
        self.logger = logger or Logger()
        self.config_file = config_file
    
    def create_backup_folder_name(self, folder_name: str, add_timestamp: bool = True) -> str:
        """
        Erstellt einen Backup-Ordnernamen mit optionalem Zeitstempel.
        
        Args:
            folder_name (str): Der Basis-Ordnername
            add_timestamp (bool): Wenn True, wird Datum/Zeit angehängt
        
        Returns:
            str: Der generierte Ordnername
        """
        if not add_timestamp:
            return folder_name
        
        try:
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M%S")
            backup_name = f"{folder_name}_backup_{current_date}_{current_time}"
            self.logger.debug(f"Generated backup folder name: {backup_name}")
            return backup_name
        except Exception as e:
            self.logger.error(f"Error generating backup folder name: {str(e)}")
            return folder_name
    
    def ensure_directory_exists(self, directory_path: str) -> Tuple[bool, str]:
        """
        Stellt sicher, dass ein Verzeichnis existiert. Erstellt es wenn nötig.
        
        Args:
            directory_path (str): Der Pfad des zu erstellenden Verzeichnisses
        
        Returns:
            Tuple[bool, str]: (Erfolg True/False, Nachricht)
        """
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Directory ensured: {directory_path}")
            return True, f"Directory created/verified: {directory_path}"
        except PermissionError:
            msg = f"Permission denied creating directory: {directory_path}"
            self.logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error creating directory {directory_path}: {str(e)}"
            self.logger.error(msg)
            return False, msg
    
    def create_zip_archive(self, source_folder: str, output_zip: Optional[str] = None) -> Tuple[bool, str]:
        """
        Erstellt ein ZIP-Archiv aus einem Ordner.
        
        Args:
            source_folder (str): Der Quellordner
            output_zip (Optional[str]): Der Pfad der ZIP-Datei. 
                                       Wenn None, wird [source_folder].zip verwendet
        
        Returns:
            Tuple[bool, str]: (Erfolg True/False, Pfad oder Fehlermeldung)
        """
        if not output_zip:
            output_zip = f"{source_folder}.zip"
        
        try:
            if not os.path.isdir(source_folder):
                msg = f"Source folder does not exist: {source_folder}"
                self.logger.error(msg)
                return False, msg
            
            self.logger.info(f"Creating ZIP archive: {output_zip}")
            
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Relative Pfad für Archive
                        arcname = os.path.relpath(file_path, source_folder)
                        zipf.write(file_path, arcname)
            
            # Dateigrößen ermitteln
            zip_size = os.path.getsize(output_zip)
            msg = f"ZIP archive created: {output_zip} ({zip_size / (1024*1024):.2f} MB)"
            self.logger.success(msg)
            return True, output_zip
            
        except PermissionError:
            msg = f"Permission denied creating ZIP: {output_zip}"
            self.logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error creating ZIP archive: {str(e)}"
            self.logger.error(msg)
            return False, msg
    
    def save_config(self, data: Dict, config_file: Optional[str] = None) -> Tuple[bool, str]:
        """
        Speichert Konfigurationsdaten als JSON.
        
        Args:
            data (Dict): Die zu speichernden Daten
            config_file (Optional[str]): Pfad zur Konfigurationsdatei.
                                        Wenn None, wird self.config_file verwendet
        
        Returns:
            Tuple[bool, str]: (Erfolg True/False, Nachricht)
        """
        if config_file is None:
            config_file = self.config_file
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.logger.debug(f"Config saved: {config_file}")
            return True, f"Configuration saved to {config_file}"
        except PermissionError:
            msg = f"Permission denied saving config: {config_file}"
            self.logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error saving config: {str(e)}"
            self.logger.error(msg)
            return False, msg
    
    def load_config(self, config_file: Optional[str] = None) -> Dict:
        """
        Lädt Konfigurationsdaten aus JSON.
        
        Args:
            config_file (Optional[str]): Pfad zur Konfigurationsdatei.
                                        Wenn None, wird self.config_file verwendet
        
        Returns:
            Dict: Die geladenen Konfigurationsdaten oder leeres Dict wenn Fehler
        """
        if config_file is None:
            config_file = self.config_file
        
        try:
            if not os.path.exists(config_file):
                self.logger.debug(f"Config file does not exist: {config_file}")
                return {}
            
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.debug(f"Config loaded: {config_file}")
            return data
            
        except json.JSONDecodeError:
            msg = f"Invalid JSON in config file: {config_file}"
            self.logger.warning(msg)
            return {}
        except Exception as e:
            msg = f"Error loading config: {str(e)}"
            self.logger.error(msg)
            return {}
    
    def delete_directory(self, directory_path: str) -> Tuple[bool, str]:
        """
        Löscht ein Verzeichnis rekursiv.
        
        Args:
            directory_path (str): Der zu löschende Verzeichnispfad
        
        Returns:
            Tuple[bool, str]: (Erfolg True/False, Nachricht)
        """
        try:
            import shutil
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
                self.logger.info(f"Directory deleted: {directory_path}")
                return True, f"Directory deleted: {directory_path}"
            else:
                msg = f"Directory not found: {directory_path}"
                self.logger.warning(msg)
                return False, msg
        except PermissionError:
            msg = f"Permission denied deleting directory: {directory_path}"
            self.logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error deleting directory: {str(e)}"
            self.logger.error(msg)
            return False, msg