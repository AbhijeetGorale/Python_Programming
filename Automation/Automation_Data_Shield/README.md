# 🛡️ Automated Data Shield

An automated backup utility written in Python that periodically backs up files from a source directory, copies only new or updated files, and creates a timestamped archive (`.zip`) for safe storage.

---

## 📌 Features
- ✅ **Incremental Backup** – Copies only new or modified files using MD5 hash comparison.
- ✅ **Automated Scheduling** – Runs backups at user‑defined time intervals (in minutes).
- ✅ **Archiving** – Creates a compressed `.zip` file of the backup folder with a timestamp.
- ✅ **Folder Structure Preservation** – Maintains the original directory hierarchy in backups.
- ✅ **Command-Line Options** – Provides help and usage instructions.

---

## 📂 Project Structure
AutomatedDataShield.py   # Main Python script
Data/                    # Example source directory (your files go here)
Backup_Folder/           # Auto-created backup folder (generated at runtime)
Backup_Folder_YYYY-MM-DD_HH-MM-SS.zip  # Timestamped archive


---

## ⚙️ Requirements
- Python 3.x
- Libraries:
  - `schedule` (install via `pip install schedule`)
  - Standard libraries: `os`, `sys`, `time`, `shutil`, `hashlib`, `zipfile`

---

## 🚀 Usage

### 1. Show Help
```bash
python AutomatedDataShield.py --h
Displays information about what the script does.

python AutomatedDataShield.py --u
Explains how to run the script with parameters.

python AutomatedDataShield.py <TimeInterval> <SourceDirectory>

TimeInterval → Time in minutes between backups

SourceDirectory → Directory you want to back up

python AutomatedDataShield.py 5 Data

This will:
Run a backup every 5 minutes.
Copy files from the Data directory into Backup_Folder.
Create a timestamped .zip archive after each backup.

After execution, you’ll see:

---------------------------------------------------------------------
Backup Process Started successfully at : Fri Jul 17 00:11:00 2026
---------------------------------------------------------------------
Backup completed successfully
Files copied : 12
Zip file gets created : Backup_Folder_year-month-date_00-00-00.zip
---------------------------------------------------------------------

🛑 Stopping the Program
Press Ctrl + C in the terminal to stop the scheduler.

🔧 Notes
The backup folder (Backup_Folder) and zip archives are created in the same directory where you run the script.

If the destination folder already exists, only new or updated files will be copied.

Archives are named with the format:
Backup_Folder_YYYY-MM-DD_HH-MM-SS.zip

## 🔄 Workflow Diagram

```mermaid

    A[Start Script] --> B{Command-line Arguments}
    B -->|--h| C[Show Help]
    B -->|--u| D[Show Usage Instructions]
    B -->|TimeInterval + SourceDir| E[Scheduler Starts]

    E --> F[Backup Process Triggered]
    F --> G[Scan Source Directory]
    G --> H[Compare Files with Backup_Folder]
    H -->|New/Updated| I[Copy Files to Backup_Folder]
    H -->|Unchanged| J[Skip File]

    I --> K[Create Timestamped Zip Archive]
    J --> K[Create Timestamped Zip Archive]

    K --> L[Log Output to Console]
    L --> M[Wait for Next Interval]
    M --> E

📝 Explanation
Start Script → Run with arguments (TimeInterval and SourceDirectory).

Scheduler → Executes backup every N minutes.

Backup Process → Scans source directory.

File Comparison → Uses MD5 hash to detect changes.

Copy Files → Only new/updated files are copied to Backup_Folder.

Archive → Creates a .zip file with timestamp.

Repeat → Scheduler waits and repeats until stopped.

📜 License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute.

👨‍💻 Author
Developed by Abhijeet Gorale  
GitHub: https://github.com/AbhijeetGorale