markdown
# Platform Surveillance System 🖥️

A Python-based **system monitoring and logging tool** that periodically generates detailed reports about CPU, RAM, Disk, Network usage, and running processes. Logs are stored in timestamped files for easy tracking.

---

## 📋 Features
- Automatic log file creation with timestamps  
- CPU and RAM usage monitoring  
- Disk usage report for all partitions  
- Network I/O statistics (sent/received data)  
- Process details (PID, name, user, status, start time, CPU%, memory%)  
- Periodic scheduling using `schedule`  
- Easy command-line usage with help and usage options  

---

## 🛠️ Requirements
- Python 3.x  
- Libraries:
  ```bash
  pip install psutil schedule
🚀 Usage
1. Help Option
Displays details about what the script does:

bash
python Demo.py --h
2. Usage Option
Explains how to run the script:

bash
python Demo.py --u
3. Run the Script
Run with a time interval (in minutes) and a folder name:

bash
python Demo.py 5 Logs
5 → Time interval in minutes (logs created every 5 minutes)

Logs → Folder name where log files will be stored

📂 Output
A folder (e.g., Logs) will be created if it doesn’t exist.

Inside, log files will be generated with names like:

Code
Report_2026-07-14_21-30-00.log
Each log file contains:

CPU usage

RAM usage

Disk usage

Network usage

Process details

⏹️ Stopping the Script
Since the script runs continuously:

Press Ctrl + C in the terminal to stop execution gracefully.

⚡ Advanced Tips
Run in background:

Linux/Mac:

bash
nohup python Demo.py 5 Logs &
Windows: Use PowerShell or Task Scheduler.

Future Enhancements:

Add email functionality to send logs automatically.

Use Python’s logging module for better log management.

Implement log rotation to avoid clutter.

📖 Example
bash
python Demo.py 10 Surveillance
This will:

Create a folder named Surveillance

Generate a log file every 10 minutes

Store system and process reports inside timestamped .log files

🙌 Credits
Developed by AbhiJeet Gorale 
Built with Python, psutil, and schedule.

🌐 GitHub: [AbhijeetGorale](https://github.com/AbhijeetGorale)

🔗 LinkedIn: www.linkedin.com/in/abhijeetgorale