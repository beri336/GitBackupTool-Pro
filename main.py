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
    update_status("", "black")
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
app.geometry("700x320")
app.minsize(700,320)
app.protocol("WM_DELETE_app", on_window_close)
center_window(app, 700, 350)

## Frames
main_frame = ctk.CTkFrame(app)
main_frame.pack(padx=5, pady=5, fill="both", expand=True)

fr_status_label = ctk.CTkFrame(main_frame)
fr_status_label.pack(padx=5, pady=4, fill="x")

fr_url = ctk.CTkFrame(main_frame)
fr_url.pack(padx=5, pady=4, fill="x")

fr_folder = ctk.CTkFrame(main_frame)
fr_folder.pack(padx=5, pady=4, fill="x")

fr_save_path = ctk.CTkFrame(main_frame)
fr_save_path.pack(padx=5, pady=4, fill="x")

fr_checkbox = ctk.CTkFrame(main_frame)
fr_checkbox.pack(padx=5, pady=4, fill="x")

fr_buttons = ctk.CTkFrame(main_frame)
fr_buttons.pack(padx=5, pady=4, fill="x")


## UI Elements
# Status label for feedback
status_label = ctk.CTkLabel(fr_status_label, text="")
status_label.pack(side="top", pady=5)

# GitHub URL input
url_label = ctk.CTkLabel(fr_url, text="GitHub URL:")
url_label.pack(side="left", padx=10, pady=(5, 0))

github_url_entry = ctk.CTkEntry(fr_url, width=300)
github_url_entry.pack(side="left", padx=10, pady=(5, 0), expand=True, fill="x")

# Folder name input
folder_label = ctk.CTkLabel(fr_folder, text="Folder Name:")
folder_label.pack(side="left", padx=10, pady=5)

folder_name_entry = ctk.CTkEntry(fr_folder, width=300)
folder_name_entry.pack(side="left", padx=10, pady=5, expand=True, fill="x")

# Path input
path_label = ctk.CTkLabel(fr_save_path, text="Save Path:")
path_label.pack(side="left", padx=10, pady=5)

path_entry = ctk.CTkEntry(fr_save_path, width=300)
path_entry.pack(side="left", padx=10, pady=5, expand=True, fill="x")

browse_button = ctk.CTkButton(fr_save_path, text="Browse", command=browse_folder)
browse_button.pack(side="left", padx=10, pady=5)

# Backup options
backup_checkbox_var = ctk.BooleanVar(value=False)
backup_checkbox = ctk.CTkCheckBox(fr_checkbox, text="Create Backup Folder", variable=backup_checkbox_var)
backup_checkbox.pack(side="top", pady=5)

zip_backup_var = ctk.BooleanVar(value=False)
zip_checkbox = ctk.CTkCheckBox(fr_checkbox, text="Create ZIP Archive", variable=zip_backup_var)
zip_checkbox.pack(side="top", pady=5)

# Action buttons
clone_button = ctk.CTkButton(fr_buttons, text="Clone", command=clone_repo_thread)
clone_button.pack(side="left", padx=5, pady=5)

clear_button = ctk.CTkButton(fr_buttons, text="Clear", command=clear_entries)
clear_button.pack(side="left", padx=5, pady=5, expand=True)

log_button = ctk.CTkButton(fr_buttons, text="View Log", command=open_log)
log_button.pack(side="right", padx=5, pady=5)

# load last used Repository
load_last_used_repo()

# start the main application loop
app.mainloop()