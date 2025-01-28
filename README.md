# README GitBackupTool-Pro

## Table of Contents

01. [Motivation](#01-motivation)
02. [Installation](#02-installation)
03. [Usage](#3-usage)
04. [Code](#4-code)
05. [Troubleshooting](#5-troubleshooting)
06. [Contributing](#6-contributing)
07. [Licence](#7-licence)
08. [Version](#8-version)

<br><hr>

## 1. Motivation

GitBackupTool-Pro was designed to simplify working with repositories. It aims to quickly clone new GitHub repositories using a user-friendly GUI or create local backups of existing repositories on GitHub. The tool is written entirely in Python with a strong focus on user experience (UX).

<br><hr>

## 2. Installation

### Prerequisites
- 1: **Git**: Ensure git is installed and added to your system's PATH. You can download it from [Git](https://git-scm.com).
- 2: **Python**: Install Python 3.8+ from [Python.org](https://www.python.org).

### Steps
1. **Clone this Repository**:
```bash
git clone https://github.com/beri336/GitBackupTool-Pro
```

2. **Navigate to the Directory**:
```bash
cd GitBackupTool-Pro
```

3. **Install Dependencies**:
```bash
pip install customtkinter
```
- or using `requirements.txt`, use:
```bash
pip install -r requirements.txt
```

<br><hr>


## 3. Usage

1. **Run the application**:
```bash
python main.py
```

- the GUI will look like this:

![GUI](<Pictures/GUI.png>)

<br>

2. **How to use it**:
> TextBox
- `GitHub URL`: Enter the URL of the GitHub repository you want to clone.
- `Folder Name`: Specify the name for the new folder where the repository will be cloned.
- `Save Path`: Define the local directory where the repository should be downloaded.

<br>

> Button
- `Browse`: This button opens a file dialog to select the location where the repository should be saved.
- `Clone`: Starts the cloning process if all three text boxes are filled.
- `Clear`: Clears all input fields in the text boxes.
- `View Log`: Displays a log file created during the download process, showing the time, repository URL, and save location.

<br>

> CheckBox
- `Create Backup Folder`: When this checkbox is selected, "Backup_" is prefixed to the folder name.
- `Create ZIP Archive`: Creates a ZIP file of the folder in addition to the regular folder.

<br>

- **Example**:

![Example Usage](</Pictures/Example.png>)

- The repository is saved to the desktop after clicking the **`Clone`** button.  
- After a repository is cloned, a `last_used_repo.json` file is created, allowing the program to automatically load the last used GitHub URL and save path when reopened.  

<br><hr>

### 4. Code

#### Functions Overview

> browse_folder
- Opens a folder dialog to select a save path and inserts the selected path into the input field.

<br>

> is_valid_repo_url
- Validates whether the provided GitHub URL corresponds to a valid and accessible repository.

<br>

> update_status
- Updates the status label with a message and color, then clears the message after 3 seconds.

<br>

> log_action
- Logs actions or errors to a `log.txt` file with timestamps for troubleshooting or record-keeping.

<br>

> zip_folder
- Creates a ZIP archive of the specified folder, including all its contents.

<br>

> clone_repo
- Clones the GitHub repository to a specified location, handles backup and ZIP options, and logs actions.

<br>

> clear_entries
- Clears all input fields and resets options to their default state.

<br>

> save_last_used_repo
- Saves the last used GitHub URL and save path to a JSON file for future reference.

<br>

> load_last_used_repo
- Loads the last saved GitHub URL and save path from a JSON file and populates the relevant fields.

<br>

> clear_status
- Clears the status label's message.

<br>

> clone_repo_thread
- Runs the `clone_repo` function in a separate thread to prevent blocking the UI during execution.

<br>

> on_window_close
- Handles the action for closing the application window.

<br>

> center_window
- Centers the application window on the user's screen.

<br>

> open_log
- Opens the `log.txt` file in the default text editor, or displays a message if the log file doesn't exist.

<br><hr>

### 5. Troubleshooting

#### **1. GitHub Repository URL Not Valid**
- **Problem:** The application displays an error: "Invalid or unreachable GitHub URL."
- **Solution:** 
  - Double-check the URL format (e.g., `https://github.com/username/repository`).
  - Ensure the repository is public or you have the necessary credentials for private repositories.
  - Confirm that Git is installed and correctly added to your system's PATH.

<br>

#### **2. Cloning Operation Fails**
- **Problem:** The cloning process stops with an error or the repository is not cloned.
- **Solution:** 
  - Verify that the target directory is writable and not already in use.
  - Ensure your internet connection is stable.
  - Check the log file (`log.txt`) for detailed error messages.
  - Test the `git clone` command manually in the terminal to confirm Git functionality.

<br>

#### **3. ZIP Archive Not Created**
- **Problem:** No ZIP file is created after enabling the "Create ZIP Archive" option.
- **Solution:** 
  - Verify that the target folder was cloned successfully before zipping.
  - Ensure you have write permissions in the target directory.
  - Check the log file for any zipping errors.

<br>

#### **4. Log File Not Found**
- **Problem:** Clicking "View Log" shows an error or no log file opens.
- **Solution:** 
  - Check if the `log.txt` file exists in the application directory.
  - Perform any action (e.g., cloning) to ensure a log entry is created.

<br>

#### **5. Last Used Repo Not Loaded**
- **Problem:** The previously saved GitHub URL and save path are not loaded on startup.
- **Solution:** 
  - Confirm that the `last_used_repo.json` file exists in the application directory.
  - Check the JSON file for proper formatting.

<br>

#### **6. GUI Layout Issues**
- **Problem:** The UI does not display correctly or elements are misaligned.
- **Solution:** 
  - Ensure you are using a compatible version of Python and `customtkinter`.
  - Try resizing the window or restarting the application.

<br>

#### **7. Permissions Error**
- **Problem:** The application cannot create or write files in the selected directory.
- **Solution:** 
  - Run the application with elevated permissions (e.g., as an Administrator on Windows).
  - Choose a directory where your user account has write access.

<br><hr>

### 6. Contributing

![Created By](</Pictures/created-by.svg>)

- Contributions are welcome! If you find bugs, have feature suggestions, or want to improve the code, please raise an issue or create a pull request.

<br><hr>

## 7. Licence
This project is licensed under the MIT License.

<br><hr>

## 8. Version
> **Version 1.0**
- Initial release with core functionality to clone GitHub repositories, create backups, generate ZIP archives, and manage logs through a user-friendly GUI.

<hr>