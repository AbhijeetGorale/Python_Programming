import hashlib
import os
import datetime
import smtplib
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SENDER_EMAIL = "Your_Email_Id"
SENDER_PASSWORD = "Your_Password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def CalculateChecksum(FileName):
    """Calculate MD5 checksum of a file."""
    with open(FileName, "rb") as fobj:
        hobj = hashlib.md5()
        Buffer = fobj.read(1000)
        while Buffer:
            hobj.update(Buffer)
            Buffer = fobj.read(1000)
    return hobj.hexdigest()

def FindDuplicate(DirectoryName):
    """Find duplicate files in a directory based on checksum."""
    if not os.path.exists(DirectoryName):
        print("There is no such directory")
        return {}
    if not os.path.isdir(DirectoryName):
        print("It is not a directory")
        return {}

    Duplicate = {}
    for FolderName, SubFolderName, Filename in os.walk(DirectoryName):
        for fname in Filename:
            fname = os.path.join(FolderName, fname)
            Checksum = CalculateChecksum(fname)
            Duplicate.setdefault(Checksum, []).append(fname)
    return Duplicate

def DisplayResult(MyDict):
    """Display duplicate files without deleting them."""
    Result = list(filter(lambda x: len(x) > 1, MyDict.values()))
    if not Result:
        print("No duplicates found.")
        return
    print("\nDuplicate files found:")
    for group in Result:
        for file in group:
            print("   ", file)
        print("-" * 40)

def SendEmailWithAttachment(LogFile, recipient_email):
    """Send the log file as a .txt email attachment to recipient."""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = "Duplicate File Deletion Report"

    body = "Please find attached the duplicate file deletion log report."
    msg.attach(MIMEText(body, "plain"))

    with open(LogFile, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(LogFile))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(LogFile)}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Log report sent successfully to {recipient_email}")
    except Exception as e:
        print("Failed to send email:", e)

def DeleteDuplicate(Path):

    log_folder = os.path.join(os.getcwd(), "Delete_Duplicate_Files")
    os.makedirs(log_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    LogFile = os.path.join(log_folder, f"DeletedFiles_{timestamp}.txt")

    MyDict = FindDuplicate(Path)
    Result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    if not Result:
        print("No duplicates to delete.")
        return

    DisplayResult(MyDict)

    choice = input("\nDo you want to delete duplicates? (yes/no): ").strip().lower()
    if choice != "yes":
        print("Deletion cancelled.")
        return

    Cnt = 0
    with open(LogFile, "w") as log:
        log.write("=== Deletion Log: {} ===\n".format(datetime.datetime.now()))
        for group in Result:
            for file in group[1:]:
                print("Deleted file:", file)
                os.remove(file)
                log.write("Deleted: {}\n".format(file))
                Cnt += 1

    print("\nTotal deleted files:", Cnt)
    print("Log saved to:", LogFile)

    email_choice = input("\nDo you want to email the log report? (yes/no): ").strip().lower()
    if email_choice == "yes":
        recipient = input("Enter recipient email: ").strip()
        SendEmailWithAttachment(LogFile, recipient)

def main():
    if len(sys.argv) < 2:
        print("Usage: python Scriptname.py <FolderName>")
        return
    folder = sys.argv[1]

    print("Press Ctrl + C anytime to stop the script safely.")

    try:
        while True:
            print("\n=== Running duplicate check at", datetime.datetime.now(), "===")
            DeleteDuplicate(folder)
            print("Next check will run in 12 hours...")
            print("Press Ctrl + C to end the deletion process if needed.")
            time.sleep(12 * 60 * 60)  # <= sleep for 12 hours 
    except KeyboardInterrupt:
        print("\nScript stopped by user (Ctrl + C). Goodbye!")

if __name__ == "__main__":
    main()
