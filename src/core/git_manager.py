# core/git_manager.py

"""
Git-Manager für alle Git-Operationen.
Verwaltet Git-Befehle und URL-Validierung.
"""

import subprocess
from typing import Tuple
from config import GIT_CLONE_TIMEOUT
from .logger import Logger


class GitManager:
    """
    Manager für Git-Operationen.
    
    Attributes:
        logger (Logger): Logger-Instanz für Logging
        timeout (int): Timeout für Git-Befehle in Sekunden
    """
    
    def __init__(self, logger: Logger = None, timeout: int = GIT_CLONE_TIMEOUT) -> None:
        """
        Initialisiert den GitManager.
        
        Args:
            logger (Logger): Logger-Instanz. Wenn None, wird eine neue erstellt
            timeout (int): Timeout für Git-Befehle. Default aus config.py
        """
        self.logger = logger or Logger()
        self.timeout = timeout
    
    def is_valid_url(self, url: str) -> bool:
        """
        Validiert, ob eine GitHub-URL erreichbar und gültig ist.
        
        Args:
            url (str): Die zu validierende GitHub-URL
        
        Returns:
            bool: True wenn URL gültig, False sonst
        """
        if not url or not isinstance(url, str):
            self.logger.warning(f"Invalid URL format: {url}")
            return False
        
        try:
            result = subprocess.run(
                ["git", "ls-remote", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=self.timeout
            )
            self.logger.info(f"URL validation successful: {url}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"URL validation failed (git error): {url} - {str(e)}")
            return False
        except subprocess.TimeoutExpired:
            self.logger.error(f"URL validation timeout: {url}")
            return False
        except FileNotFoundError:
            self.logger.error("Git is not installed or not in PATH")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during URL validation: {str(e)}")
            return False
    
    def clone(self, url: str, target_path: str) -> Tuple[bool, str]:
        """
        Klont ein GitHub-Repository zu einem bestimmten Pfad.
        
        Args:
            url (str): Die GitHub-URL des zu klonenden Repositories
            target_path (str): Der Zielpfad für das Repository
        
        Returns:
            Tuple[bool, str]: (Erfolg True/False, Nachricht)
        """
        if not url or not target_path:
            msg = "URL or target path is empty"
            self.logger.error(msg)
            return False, msg
        
        try:
            self.logger.info(f"Starting clone: {url} -> {target_path}")
            
            subprocess.run(
                ["git", "clone", url, target_path],
                check=True,
                capture_output=True,
                timeout=None  # Clone kann länger dauern
            )
            
            msg = f"Successfully cloned: {url}"
            self.logger.success(msg)
            return True, msg
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Git clone failed: {str(e.stderr.decode() if e.stderr else e)}"
            self.logger.error(error_msg)
            return False, error_msg
        except FileNotFoundError:
            error_msg = "Git command not found. Please ensure Git is installed."
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during clone: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg