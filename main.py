import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from datetime import datetime
import json
import platform

def browse_folder():
    ''' Opens FileDialog to choose path. '''
    folder_selected = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_selected)

def clone_repo(event=None):
    ''' Clone the GitHub Repository. '''
    github_url = github_url_entry.get()
    folder_name = folder_name_entry.get()
    target_path = path_entry.get()
    add_backup = backup_checkbox_var.get() # check if backup checkbox is checked

    if not github_url or not folder_name or not target_path:
        status_label.config(text="Please fill in all fields", fg="red")
        success_label.config(text="")
        root.after(3000, clear_status) # delete error message after 3 seconds
        return

    current_date = datetime.now().strftime("%Y%m%d") # current date
    current_time = datetime.now().strftime("%H%M%S") # current time
    if add_backup:
        backup_folder_name = f"{folder_name}_backup_{current_date}_{current_time}"
    else:
        backup_folder_name = folder_name
    target_directory = os.path.join(target_path, backup_folder_name)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    try:
        subprocess.run(["git", "clone", github_url, target_directory], check=True)
        status_label.config(text="")
        success_label.config(text="Repository successfully cloned!", fg="green")
        root.after(3000, clear_status)
        save_last_used_repo(github_url, target_path)
    except subprocess.CalledProcessError as e:
        status_label.config(text=f"Fehler: {e}", fg="red")
        success_label.config(text="")
        root.after(3000, clear_status)

def clear_entries():
    ''' Remove all text from Text Entry. '''
    github_url_entry.delete(0, tk.END)
    folder_name_entry.delete(0, tk.END)
    path_entry.delete(0, tk.END)
    status_label.config(text="")
    success_label.config(text="")
    backup_checkbox_var.set(True) # reset checkbox to checked state

def save_last_used_repo(github_url, path):
    ''' Save the GitHub URL and save path for faster backup creation as JSON. '''
    data = {
        "github_url": github_url,
        "path": path
    }
    with open("last_used_repo.json", "w") as json_file:
        json.dump(data, json_file)

def load_last_used_repo():
    ''' Load the last used JSON, if it exists. '''
    if os.path.exists("last_used_repo.json"):
        with open("last_used_repo.json", "r") as json_file:
            data = json.load(json_file)
            github_url_entry.insert(0, data.get("github_url", ""))
            path_entry.insert(0, data.get("path", ""))

def open_settings(event=None):
    ''' Open and save the path location. '''
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("680x100")  # fixed size
    settings_window.resizable(False, False)  # fixed size

    def save_settings():
        new_json_path = json_path_entry.get()
        if new_json_path:
            settings_window.destroy()

    tk.Label(settings_window, text="JSON-File-Path:").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="e")
    json_path_entry = tk.Entry(settings_window, width=40)
    json_path_entry.insert(tk.END, "last_used_repo.json")
    json_path_entry.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="we")

    browse_json_button = tk.Button(settings_window, text="Browse",
                                   command=lambda: json_path_entry.insert(tk.END, filedialog.askopenfilename()))
    browse_json_button.grid(row=0, column=2, padx=10, pady=(10, 5))

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=1, column=1, pady=10)

def on_enter(event):
    clone_button.config(bg="#90EE90")

def on_leave(event):
    clone_button.config(bg="SystemButtonFace")

def clear_status():
    ''' Clear Labels. '''
    status_label.config(text="")
    success_label.config(text="")

def on_window_close():
    ''' Action when the window is closed. '''
    root.destroy()

def center_window(width, height):
    ''' Function for centering the main window. '''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x_position}+{y_position}")

# create main window
root = tk.Tk()
root.minsize(400, 300)
root.title("GitBackupTool Pro")
root.protocol("WM_DELETE_root", on_window_close)
center_window(700, 300)

# shortcut for opening Settings
current_os = platform.system()
if current_os == "Darwin": # Mac
    root.bind("<Command-comma>", open_settings)
else: # Windows und Linux
    root.bind("<Control-comma>", open_settings)

# status label
status_label = tk.Label(root, text="")
status_label.grid(row=0, column=0, columnspan=3, pady=(5, 0), sticky="we")

# success label
success_label = tk.Label(root, text="")
success_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="we")

# GitHub URL input
tk.Label(root, text="GitHub URL:").grid(row=2, column=0, padx=10, pady=(5, 0), sticky="e")
github_url_entry = tk.Entry(root, width=50)
github_url_entry.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="we")

# enter folder name
tk.Label(root, text="File name:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
folder_name_entry = tk.Entry(root, width=50)
folder_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

# path input
tk.Label(root, text="Save Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
path_entry = tk.Entry(root, width=50)
path_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

# backup checkbox
backup_checkbox_var = tk.BooleanVar()
backup_checkbox_var.set(True)  # Default value checked
backup_checkbox = tk.Checkbutton(root, text="Create Backup",
                                 variable=backup_checkbox_var,
                                 onvalue=True, offvalue=False)
backup_checkbox.grid(row=5, column=0, columnspan=3)

# browse button
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=4, column=2, columnspan=3, padx=10, pady=5)

# clone Button
clone_button = tk.Button(root, text="Clone", command=clone_repo)
clone_button.grid(row=7, column=0, columnspan=3, pady=10)

# bind events for hover effect
clone_button.bind("<Enter>", on_enter)
clone_button.bind("<Leave>", on_leave)

# clear Button
clear_button = tk.Button(root, text="Clear", command=clear_entries)
clear_button.grid(row=2, column=3, columnspan=3, padx= 10, pady=10)

# load last used repository, if available
load_last_used_repo()

# configure grid to scale with the window
for i in range(9):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(1, weight=1)

# menu bar
menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

# execute application
root.mainloop()