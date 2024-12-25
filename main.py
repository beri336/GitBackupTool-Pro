import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
from datetime import datetime
import json
import zipfile
import platform

def browse_folder():
    ''' Opens FileDialog to choose path. '''
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, ctk.END)
        path_entry.insert(0, folder_selected)

def is_valid_repo_url(url):
    """Prüft, ob die GitHub-URL ein gültiges Repository ist."""
    try:
        subprocess.run(["git", "ls-remote", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_status(message, color):
    status_label.configure(text=message, text_color=color)
    root.after(3000, clear_status)

def log_action(action):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {action}\n")

def zip_folder(folder_path):
    zip_name = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), folder_path))
    log_action(f"Created ZIP archive: {zip_name}")

def clone_repo():
    ''' Clone the GitHub Repository. '''
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
    ''' Remove all text from Text Entry. '''
    github_url_entry.delete(0, ctk.END)
    folder_name_entry.delete(0, ctk.END)
    path_entry.delete(0, ctk.END)
    update_status("", "")
    backup_checkbox_var.set(True)

def save_last_used_repo(github_url, path):
    ''' Save the GitHub URL and save path for faster backup creation as JSON. '''
    data = {
        "github_url": github_url,
        "path": path
    }
    json_file_path = os.path.abspath("last_used_repo.json")
    
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file)
    
    print(f"Last used repo saved to: {json_file_path}")

def load_last_used_repo():
    ''' Load the last used JSON, if it exists. '''
    if os.path.exists("last_used_repo.json"):
        with open("last_used_repo.json", "r") as json_file:
            data = json.load(json_file)
            github_url_entry.insert(0, data.get("github_url", ""))
            path_entry.insert(0, data.get("path", ""))

def clear_status():
    ''' Reset status label. '''
    status_label.configure(text="")

def on_window_close():
    ''' Action when the window is closed. '''
    root.destroy()

def center_window(app, width, height):
    ''' Center window when running program. '''
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    app.geometry(f"{width}x{height}+{x_position}+{y_position}")

def open_log():
    if os.path.exists("log.txt"):
        os.system("notepad log.txt" if platform.system() == "Windows" else "open log.txt")
    else:
        messagebox.showinfo("Info", "Log file not found.")


# Main Application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("GitBackupTool Pro")
root.protocol("WM_DELETE_root", on_window_close)
root.geometry("700x350")
center_window(root, 700, 350)

# Status Labels
status_label = ctk.CTkLabel(root, text="")
status_label.grid(row=0, column=0, columnspan=3, pady=(5, 0), sticky="we")

# GitHub URL Input
ctk.CTkLabel(root, text="GitHub URL:").grid(row=1, column=0, padx=10, pady=(5, 0), sticky="e")
github_url_entry = ctk.CTkEntry(root, width=300)
github_url_entry.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="we")

# Folder Name Input
ctk.CTkLabel(root, text="Folder Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
folder_name_entry = ctk.CTkEntry(root, width=300)
folder_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

# Path Input
ctk.CTkLabel(root, text="Save Path:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
path_entry = ctk.CTkEntry(root, width=300)
path_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

# Browse Button
browse_button = ctk.CTkButton(root, text="Browse", command=browse_folder)
browse_button.grid(row=3, column=2, padx=10, pady=5)

# Backup Options
backup_checkbox_var = ctk.BooleanVar(value=False)
backup_checkbox = ctk.CTkCheckBox(root, text="Create Backup Folder", variable=backup_checkbox_var)
backup_checkbox.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)

zip_backup_var = ctk.BooleanVar(value=False)
zip_checkbox = ctk.CTkCheckBox(root, text="Create ZIP Archive", variable=zip_backup_var)
zip_checkbox.grid(row=4, column=2, columnspan=2, sticky="w", padx=10, pady=5)

# Clone Button
clone_button = ctk.CTkButton(root, text="Clone", command=clone_repo)
clone_button.grid(row=5, column=0, columnspan=3, pady=10)

# Clear Button
clear_button = ctk.CTkButton(root, text="Clear", command=clear_entries)
clear_button.grid(row=6, column=0, columnspan=3, pady=5)

# Open Log Button
log_button = ctk.CTkButton(root, text="View Log", command=open_log)
log_button.grid(row=7, column=0, columnspan=3, pady=5)

# Load Last Used Repository
load_last_used_repo()

# Responsiveness
root.grid_columnconfigure(1, weight=1)

# Mainloop
root.mainloop()