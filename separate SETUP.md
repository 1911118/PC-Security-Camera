```markdown
## How to Use the Script

This script runs on **Windows** and captures a webcam photo on events like PC unlock, lock, or logon. It then emails the photo with approximate location info (via public IP). It requires Python setup.

**Important Security Warning:**  
The original script has hardcoded email credentials — this is highly insecure! **Never commit or share the script with real credentials.** Always use environment variables (explained below). As of 2025, "Less secure app access" is completely disabled by Google. You **must** use a Gmail App Password.

### 1. Install Requirements

- Download and install Python 3.12+ from [python.org](https://www.python.org/downloads/) (check "Add Python to PATH" during installation).

- Open Command Prompt and install required libraries:
  ```
  pip install opencv-python requests
  ```
  (The script uses `cv2` for webcam access, `requests` for location lookup, and built-in `smtplib` for email.)

### 2. Secure Your Email Credentials (Mandatory)

- Edit the script to remove hardcoded credentials:
  ```python
  import os  # Add this at the top if not already present

  EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
  EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
  EMAIL_RECEIVER = "your_receiver_email@example.com"  # Hardcode only the receiver or also use env var
  ```

- **Set up Gmail App Password (required since Less Secure Apps are disabled):**
  1. Enable **2-Step Verification** on your Google Account: Go to [myaccount.google.com/security](https://myaccount.google.com/security) → "2-Step Verification" → Turn it on.
  2. Generate an **App Password**:
     - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
     - Select app: "Mail", Select device: "Other (Custom name)" → Name it e.g., "Security Script".
     - Copy the 16-character password generated.
  3. Set environment variables on Windows:
     - Search for "Environment Variables" in the Start menu.
     - Under "User variables", add:
       - `EMAIL_SENDER` → your Gmail address (e.g., `you@gmail.com`)
       - `EMAIL_PASSWORD` → the 16-character App Password (not your main password!)

- Use the same Gmail for sender (or a different one if you prefer).

### 3. Test the Script Manually

- Save the modified script as `security_camera.py`.
- Open Command Prompt and navigate to the script's folder:
  ```
  cd C:\Path\To\Your\Script\Folder
  ```
- Run a test:
  ```
  python security_camera.py test
  ```
- It should:
  - Create folders `C:\SecurityCaptures` and `C:\SecurityScript` if needed.
  - Capture a photo (saved in `C:\SecurityCaptures`).
  - Fetch approximate location via IP.
  - Send an email with the photo.
- Check console output, the captures folder for photos/logs, and your inbox.

### 4. Set Up Automatic Triggers with Task Scheduler

- Open **Task Scheduler** (search in Start menu).
- Click "Create Task" (not Basic Task for more options):
  - **General tab**: Name it e.g., "Security Camera on Unlock". Check "Run with highest privileges".
  - **Triggers tab**: New → Begin the task: "On workstation unlock" (or "On workstation lock", "At log on of any user").
  - **Actions tab**: New → Action: "Start a program" →
    - Program/script: Browse to `python.exe` (usually `C:\Users\YourUser\AppData\Local\Programs\Python\Python312\python.exe` or similar).
    - Add arguments: `C:\Path\To\security_camera.py unlock` (change "unlock" to "lock" or "logon" as needed).
  - **Conditions tab**: Uncheck "Start the task only if the computer is on AC power" (useful for laptops).
  - **Settings tab**: Check "Hidden" if you don't want a console window to flash.
- Save the task (may prompt for admin password).
- Test: Lock and unlock your PC — you should receive an email.

Create separate tasks for lock/logon if desired.

### 5. Troubleshooting

- **Webcam not working?** Ensure it's enabled, not in use by another app, and privacy settings allow access. The script tries camera indexes 0-2.
- **Email fails?** Double-check App Password, 2FA enabled, and environment variables. Test SMTP manually if needed.
- **No photo but email sent?** Camera unavailable — script still sends location info.
- **Folders not created/Permissions?** Run Command Prompt as Administrator for first test.
- **Debug logs:** Check `C:\SecurityScript\task_debug.log` and `C:\SecurityCaptures\security_log.txt`.
- **Location inaccurate?** It's based on public IP (not GPS).

Enjoy your basic PC security monitor! If you improve the script, feel free to contribute via pull request.
``` 
