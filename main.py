import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
from datetime import datetime
import json
import zipfile
import platform
import threading


def browse_folder():
    """ Opens a folder dialog for selecting the save path. """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, ctk.END)
        path_entry.insert(0, folder_selected)

def is_valid_repo_url(url):
    """ Validates if the provided GitHub URL is a valid repository. """
    try:
        subprocess.run(["git", "ls-remote", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_status(message, color):
    """ Updates the status label with a message and clears it after 3 seconds. """
    status_label.configure(text=message, text_color=color)
    app.after(3000, clear_status)

def log_action(action):
    """ Logs actions or errors to a log file. """
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {action}\n")

def zip_folder(folder_path):
    """ Creates a ZIP archive for the specified folder. """
    zip_name = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for app, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(app, file),
                           os.path.relpath(os.path.join(app, file), folder_path))
    log_action(f"Created ZIP archive: {zip_name}")

def clone_repo():
    """ Clones the GitHub repository and handles backup and ZIP options. """
    github_url = github_url_entry.get()
    folder_name = folder_name_entry.get()
    target_path = path_entry.get()
    add_backup = backup_checkbox_var.get()

    if not github_url or not folder_name or not target_path:
        update_status("Please fill in all fields", "red")
        return

    if not is_valid_repo_url(github_url):
        update_status("Invalid or unreachable GitHub URL", "red")
        log_action(f"Invalid GitHub URL: {github_url}")
        return

    current_date = datetime.now().strftime("%Y%m%d")
    current_time = datetime.now().strftime("%H%M%S")
    backup_folder_name = f"{folder_name}_backup_{current_date}_{current_time}" if add_backup else folder_name
    target_directory = os.path.join(target_path, backup_folder_name)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    try:
        subprocess.run(["git", "clone", github_url, target_directory], check=True)
        if zip_backup_var.get():
            zip_folder(target_directory)
        update_status("Repository successfully cloned!", "green")
        save_last_used_repo(github_url, target_path)
        log_action(f"Cloned {github_url} into {target_directory}")
    except subprocess.CalledProcessError as e:
        update_status(f"Error: {e}", "red")
        log_action(f"Error cloning {github_url}: {e}")

def clear_entries():
    """ Clears all input fields and resets options. """
    github_url_entry.delete(0, ctk.END)
    folder_name_entry.delete(0, ctk.END)
    path_entry.delete(0, ctk.END)
    update_status("", "")
    backup_checkbox_var.set(True)

def save_last_used_repo(github_url, path):
    """ Saves the last used GitHub URL and path to a JSON file. """
    data = {
        "github_url": github_url,
        "path": path
    }
    json_file_path = os.path.abspath("last_used_repo.json")
    
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file)
    
    print(f"Last used repo saved to: {json_file_path}")

def load_last_used_repo():
    """ Loads the last saved GitHub URL and path from a JSON file. """
    if os.path.exists("last_used_repo.json"):
        with open("last_used_repo.json", "r") as json_file:
            data = json.load(json_file)
            github_url_entry.insert(0, data.get("github_url", ""))
            path_entry.insert(0, data.get("path", ""))

def clear_status():
    """ Clears the status label. """
    status_label.configure(text="")

def clone_repo_thread():
    """Runs the clone_repo logic in a separate thread."""
    thread = threading.Thread(target=clone_repo)
    thread.daemon = True # ensures the thread will close when the main program exits
    thread.start()

def on_window_close():
    """ Action when the window is closed. """
    app.destroy()

def center_window(app, width, height):
    """ Center window when running program. """
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    app.geometry(f"{width}x{height}+{x_position}+{y_position}")

def open_log():
    """ Opens the log file in the default text editor. """
    if os.path.exists("log.txt"):
        os.system("notepad log.txt" if platform.system() == "Windows" else "open log.txt")
    else:
        messagebox.showinfo("Info", "Log file not found.")


# GUI setup - Main Application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("GitBackupTool Pro")
app.protocol("WM_DELETE_app", on_window_close)
app.geometry("700x350")
center_window(app, 700, 350)

## UI Elements
# Status Label
status_label = ctk.CTkLabel(app, text="")
status_label.grid(row=0, column=0, columnspan=3, pady=(5, 0), sticky="we")

# GitHub URL Input
ctk.CTkLabel(app, text="GitHub URL:").grid(row=1, column=0, padx=10, pady=(5, 0), sticky="e")
github_url_entry = ctk.CTkEntry(app, width=300)
github_url_entry.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="we")

# Folder Name Input
ctk.CTkLabel(app, text="Folder Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
folder_name_entry = ctk.CTkEntry(app, width=300)
folder_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

# Path Input
ctk.CTkLabel(app, text="Save Path:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
path_entry = ctk.CTkEntry(app, width=300)
path_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

# Browse Button
browse_button = ctk.CTkButton(app, text="Browse", command=browse_folder)
browse_button.grid(row=3, column=2, padx=10, pady=5)

# Backup Options
backup_checkbox_var = ctk.BooleanVar(value=False)
backup_checkbox = ctk.CTkCheckBox(app, text="Create Backup Folder", variable=backup_checkbox_var)
backup_checkbox.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)

zip_backup_var = ctk.BooleanVar(value=False)
zip_checkbox = ctk.CTkCheckBox(app, text="Create ZIP Archive", variable=zip_backup_var)
zip_checkbox.grid(row=4, column=2, columnspan=2, sticky="w", padx=10, pady=5)

# Action Buttoms
clone_button = ctk.CTkButton(app, text="Clone", command=clone_repo_thread)
clone_button.grid(row=5, column=0, columnspan=3, pady=10)

clear_button = ctk.CTkButton(app, text="Clear", command=clear_entries)
clear_button.grid(row=6, column=0, columnspan=3, pady=5)

log_button = ctk.CTkButton(app, text="View Log", command=open_log)
log_button.grid(row=7, column=0, columnspan=3, pady=5)

# Load last used Repository
load_last_used_repo()

# Responsiveness
app.grid_columnconfigure(1, weight=1)

# Mainloop
app.mainloop()