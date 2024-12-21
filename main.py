import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os
from datetime import datetime
import json

def browse_folder():
    ''' Opens FileDialog to choose path. '''
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, ctk.END)
        path_entry.insert(0, folder_selected)

def clone_repo():
    ''' Clone the GitHub Repository. '''
    github_url = github_url_entry.get()
    folder_name = folder_name_entry.get()
    target_path = path_entry.get()
    add_backup = backup_checkbox_var.get()

    if not github_url or not folder_name or not target_path:
        status_label.configure(text="Please fill in all fields", text_color="red")
        success_label.configure(text="")
        root.after(3000, clear_status)

        return

    current_date = datetime.now().strftime("%Y%m%d")
    current_time = datetime.now().strftime("%H%M%S")

    if add_backup:
        backup_folder_name = f"{folder_name}_backup_{current_date}_{current_time}"
    else:
        backup_folder_name = folder_name
    target_directory = os.path.join(target_path, backup_folder_name)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    try:
        subprocess.run(["git", "clone", github_url, target_directory], check=True)
        status_label.configure(text="")
        success_label.configure(text="Repository successfully cloned!", text_color="green")
        root.after(3000, clear_status)
        save_last_used_repo(github_url, target_path)
    except subprocess.CalledProcessError as e:
        status_label.configure(text=f"Error: {e}", text_color="red")
        success_label.configure(text="")
        root.after(4000, clear_status)

def clear_entries():
    ''' Remove all text from Text Entry. '''
    github_url_entry.delete(0, ctk.END)
    folder_name_entry.delete(0, ctk.END)
    path_entry.delete(0, ctk.END)
    status_label.configure(text="")
    success_label.configure(text="")
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
    success_label.configure(text="")

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


# Main Application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("GitBackupTool Pro")
root.protocol("WM_DELETE_root", on_window_close)
center_window(root, 700, 350)

# Status Labels
status_label = ctk.CTkLabel(root, text="")
status_label.grid(row=0, column=0, columnspan=3, pady=(5, 0), sticky="we")

success_label = ctk.CTkLabel(root, text="")
success_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="we")

# GitHub URL Input
ctk.CTkLabel(root, text="GitHub URL:").grid(row=2, column=0, padx=10, pady=(5, 0), sticky="e")
github_url_entry = ctk.CTkEntry(root, width=300)
github_url_entry.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="we")

# Folder Name Input
ctk.CTkLabel(root, text="Folder Name:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
folder_name_entry = ctk.CTkEntry(root, width=300)
folder_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

# Path Input
ctk.CTkLabel(root, text="Save Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
path_entry = ctk.CTkEntry(root, width=300)
path_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

# Browse Button
browse_button = ctk.CTkButton(root, text="Browse", command=browse_folder)
browse_button.grid(row=4, column=2, padx=10, pady=5)

# Backup Checkbox
backup_checkbox_var = ctk.BooleanVar(value=True)
backup_checkbox = ctk.CTkCheckBox(root, text="Create Backup", variable=backup_checkbox_var)
backup_checkbox.grid(row=5, column=0, columnspan=3)

# Clone Button
clone_button = ctk.CTkButton(root, text="Clone", command=clone_repo)
clone_button.grid(row=6, column=0, columnspan=3, pady=10)

# Clear Button
clear_button = ctk.CTkButton(root, text="Clear", command=clear_entries)
clear_button.grid(row=2, column=2, padx=10, pady=10)

# Load Last Used Repository
load_last_used_repo()

# Configure Grid for Responsiveness
root.grid_columnconfigure(1, weight=1)

# Run the Application
root.mainloop()