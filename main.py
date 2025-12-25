# main.py

from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFileDialog, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QPalette, QColor

import subprocess
import platform
import zipfile
import json
import sys
import os


class CloneWorker(QThread):
    """Worker thread for cloning repositories without blocking the UI."""
    finished = Signal(bool, str)
    
    def __init__(self, github_url, folder_name, target_path, add_backup, create_zip):
        super().__init__()
        self.github_url = github_url
        self.folder_name = folder_name
        self.target_path = target_path
        self.add_backup = add_backup
        self.create_zip = create_zip
    
    def run(self):
        try:
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M%S")
            backup_folder_name = (
                f"{self.folder_name}_backup_{current_date}_{current_time}" 
                if self.add_backup else self.folder_name
            )
            target_directory = os.path.join(self.target_path, backup_folder_name)
            
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            
            subprocess.run(
                ["git", "clone", self.github_url, target_directory], 
                check=True,
                capture_output=True
            )
            
            if self.create_zip:
                self._zip_folder(target_directory)
            
            self._log_action(f"Cloned {self.github_url} into {target_directory}")
            self.finished.emit(True, "Repository successfully cloned!")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error: {str(e)}"
            self._log_action(f"Error cloning {self.github_url}: {e}")
            self.finished.emit(False, error_msg)
        except Exception as e:
            self.finished.emit(False, f"Unexpected error: {str(e)}")
    
    def _zip_folder(self, folder_path):
        """Creates a ZIP archive for the specified folder."""
        zip_name = f"{folder_path}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        self._log_action(f"Created ZIP archive: {zip_name}")
    
    def _log_action(self, action):
        """Logs actions to a log file."""
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - {action}\n")


class ModernLineEdit(QLineEdit):
    """Custom line edit with modern styling."""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 10px 15px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #323232;
            }
            QLineEdit:hover {
                background-color: #323232;
            }
        """)


class ModernButton(QPushButton):
    """Custom button with modern styling and hover effects."""
    def __init__(self, text, primary=False, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self._setup_style()
    
    def _setup_style(self):
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
                QPushButton:disabled {
                    background-color: #2b2b2b;
                    color: #666666;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
                QPushButton:pressed {
                    background-color: #2d2d2d;
                }
            """)


class ModernCheckBox(QCheckBox):
    """Custom checkbox with modern styling."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid #3d3d3d;
                background-color: #2b2b2b;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #4CAF50;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                image: url(none);
            }
        """)


class StatusLabel(QLabel):
    """Animated status label for user feedback."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.hide()
    
    def show_message(self, message, success=True):
        """Display a status message with color coding."""
        color = "#4CAF50" if success else "#f44336"
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color}20;
                color: {color};
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid {color};
            }}
        """)
        self.setText(message)
        self.show()
        
        # Auto-hide after 3 seconds
        QTimer.singleShot(3000, self.hide)


class GitBackupToolPro(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitBackupTool Pro")
        self.setMinimumSize(750, 550)
        self.resize(750, 550)
        self._setup_ui()
        self._load_last_used_repo()
        self._center_window()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("GitBackupTool Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title)
        
        # Status label
        self.status_label = StatusLabel()
        main_layout.addWidget(self.status_label)
        
        # GitHub URL
        url_layout = QVBoxLayout()
        url_layout.setSpacing(8)
        url_label = QLabel("GitHub Repository URL")
        url_label.setStyleSheet("color: #b0b0b0; font-size: 13px;")
        self.github_url_entry = ModernLineEdit("https://github.com/username/repository")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.github_url_entry)
        main_layout.addLayout(url_layout)
        
        # Folder name
        folder_layout = QVBoxLayout()
        folder_layout.setSpacing(8)
        folder_label = QLabel("Local Folder Name")
        folder_label.setStyleSheet("color: #b0b0b0; font-size: 13px;")
        self.folder_name_entry = ModernLineEdit("my-project")
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_name_entry)
        main_layout.addLayout(folder_layout)
        
        # Save path
        path_layout = QVBoxLayout()
        path_layout.setSpacing(8)
        path_label = QLabel("Save Location")
        path_label.setStyleSheet("color: #b0b0b0; font-size: 13px;")
        
        path_input_layout = QHBoxLayout()
        path_input_layout.setSpacing(10)
        self.path_entry = ModernLineEdit("/path/to/save")
        browse_button = ModernButton("Browse")
        browse_button.clicked.connect(self._browse_folder)
        browse_button.setFixedWidth(120)
        
        path_input_layout.addWidget(self.path_entry)
        path_input_layout.addWidget(browse_button)
        
        path_layout.addWidget(path_label)
        path_layout.addLayout(path_input_layout)
        main_layout.addLayout(path_layout)
        
        # Options frame
        options_frame = QFrame()
        options_frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(10)
        
        self.backup_checkbox = ModernCheckBox("Create timestamped backup folder")
        self.zip_checkbox = ModernCheckBox("Create ZIP archive after cloning")
        
        options_layout.addWidget(self.backup_checkbox)
        options_layout.addWidget(self.zip_checkbox)
        main_layout.addWidget(options_frame)
        
        # Spacer
        main_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.clone_button = ModernButton("Clone Repository", primary=True)
        self.clone_button.clicked.connect(self._clone_repo)
        
        clear_button = ModernButton("Clear All")
        clear_button.clicked.connect(self._clear_entries)
        
        log_button = ModernButton("View Log")
        log_button.clicked.connect(self._open_log)
        
        button_layout.addWidget(self.clone_button, stretch=2)
        button_layout.addWidget(clear_button, stretch=1)
        button_layout.addWidget(log_button, stretch=1)
        
        main_layout.addLayout(button_layout)
    
    def _center_window(self):
        """Center the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def _browse_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Save Location")
        if folder:
            self.path_entry.setText(folder)
    
    def _is_valid_repo_url(self, url):
        """Validate if the GitHub URL is reachable."""
        try:
            subprocess.run(
                ["git", "ls-remote", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False
    
    def _clone_repo(self):
        """Start the repository cloning process."""
        github_url = self.github_url_entry.text().strip()
        folder_name = self.folder_name_entry.text().strip()
        target_path = self.path_entry.text().strip()
        
        # Validation
        if not github_url or not folder_name or not target_path:
            self.status_label.show_message("Please fill in all fields", success=False)
            return
        
        if not self._is_valid_repo_url(github_url):
            self.status_label.show_message("Invalid or unreachable GitHub URL", success=False)
            self._log_action(f"Invalid GitHub URL: {github_url}")
            return
        
        # Disable button during cloning
        self.clone_button.setEnabled(False)
        self.clone_button.setText("Cloning...")
        
        # Start worker thread
        self.worker = CloneWorker(
            github_url,
            folder_name,
            target_path,
            self.backup_checkbox.isChecked(),
            self.zip_checkbox.isChecked()
        )
        self.worker.finished.connect(self._on_clone_finished)
        self.worker.start()
    
    def _on_clone_finished(self, success, message):
        """Handle completion of cloning operation."""
        self.clone_button.setEnabled(True)
        self.clone_button.setText("Clone Repository")
        self.status_label.show_message(message, success=success)
        
        if success:
            self._save_last_used_repo(
                self.github_url_entry.text(),
                self.path_entry.text()
            )
    
    def _clear_entries(self):
        """Clear all input fields."""
        self.github_url_entry.clear()
        self.folder_name_entry.clear()
        self.path_entry.clear()
        self.backup_checkbox.setChecked(False)
        self.zip_checkbox.setChecked(False)
        self.status_label.hide()
    
    def _save_last_used_repo(self, github_url, path):
        """Save last used repository information."""
        data = {"github_url": github_url, "path": path}
        with open("last_used_repo.json", "w") as f:
            json.dump(data, f)
    
    def _load_last_used_repo(self):
        """Load previously used repository information."""
        if os.path.exists("last_used_repo.json"):
            try:
                with open("last_used_repo.json", "r") as f:
                    data = json.load(f)
                    self.github_url_entry.setText(data.get("github_url", ""))
                    self.path_entry.setText(data.get("path", ""))
            except json.JSONDecodeError:
                pass
    
    def _open_log(self):
        """Open the log file in the default editor."""
        if os.path.exists("log.txt"):
            if platform.system() == "Windows":
                os.system("notepad log.txt")
            elif platform.system() == "Darwin":
                os.system("open log.txt")
            else:
                os.system("xdg-open log.txt")
        else:
            self.status_label.show_message("Log file not found", success=False)
    
    def _log_action(self, action):
        """Log an action to the log file."""
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - {action}\n")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(43, 43, 43))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(76, 175, 80))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    window = GitBackupToolPro()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
