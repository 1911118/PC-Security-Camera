```markdown
# PC Security Camera — Clear Setup & Usage Instructions

Repository: [PC-Security-Camera](https://github.com/1911118/PC-Security-Camera.git)

This script (Windows) captures a webcam photo when the PC is unlocked/locked/or a user logs on, looks up approximate location by public IP, and emails the photo. It requires Python and some Windows configuration.

IMPORTANT SECURITY WARNING
- Never store real email passwords in the script. Do NOT commit credentials to the repository.
- Use environment variables and a Gmail App Password (Google has disabled "less secure apps"). You must enable 2‑Step Verification and create an App Password if using Gmail.

1. Prerequisites
- Windows 10/11.
- Python 3.12+ installed (download: https://www.python.org/downloads/). During install check “Add Python to PATH”.
- A working webcam.
- A Gmail account with 2‑Step Verification enabled and an App Password (if using Gmail as sender).

2. Install required Python packages
Open Command Prompt (or PowerShell) and run:
```
pip install opencv-python requests
```
- The script uses `cv2` (OpenCV) for webcam capture and `requests` for IP/location lookup. Email sending uses Python's built-in `smtplib`.

3. Secure your email credentials (MANDATORY)
- Modify the script to read credentials from environment variables instead of hardcoding. Example at top of the script:
```python
import os

EMAIL_SENDER = os.environ.get('EMAIL_SENDER')       # e.g. you@gmail.com
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')   # App Password (16 chars) for Gmail
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')   # recipient (or hardcode only receiver)
```
- Create a Gmail App Password:
  1. Turn on 2‑Step Verification: https://myaccount.google.com/security → "2-Step Verification".
  2. Create an App Password: https://myaccount.google.com/apppasswords  
     - Select App = "Mail", Device = "Other (Custom name)" → name it (e.g., "PC Security Script").
     - Copy the 16‑character App Password.

- Set environment variables on Windows (choose one):

  a) Using GUI:
  - Search "Edit environment variables for your account" → User variables → New:
    - Variable name: EMAIL_SENDER
      Value: you@gmail.com
    - Variable name: EMAIL_PASSWORD
      Value: (the 16-character App Password)
    - Variable name: EMAIL_RECEIVER
      Value: recipient@example.com

  b) Using Command Prompt (persistent for current user):
  ```
  setx EMAIL_SENDER "you@gmail.com"
  setx EMAIL_PASSWORD "your_app_password_here"
  setx EMAIL_RECEIVER "recipient@example.com"
  ```
  After setx, open a new Command Prompt / PowerShell window to see the variables.

  c) Temporary for current session (not persistent):
  - Command Prompt:
    ```
    set EMAIL_SENDER=you@gmail.com
    set EMAIL_PASSWORD=your_app_password_here
    set EMAIL_RECEIVER=recipient@example.com
    ```
  - PowerShell:
    ```
    $env:EMAIL_SENDER="you@gmail.com"
    $env:EMAIL_PASSWORD="your_app_password_here"
    $env:EMAIL_RECEIVER="recipient@example.com"
    ```

4. Save and test the script manually
- Save the script as: security_camera.py (in a folder you control).
- Open a new Command Prompt and navigate to the folder:
```
cd C:\Path\To\Your\Script
```
- Run a manual test:
```
python security_camera.py test
```
Expected behavior:
- The script creates folders if needed (e.g., C:\SecurityCaptures, C:\SecurityScript).
- It captures a photo (saved in C:\SecurityCaptures).
- Looks up approximate location via public IP.
- Sends an email with the photo attached.
- Check the console output, the captures folder, and your email inbox.

5. Configure automatic triggers with Task Scheduler
- Open Task Scheduler (search in Start).
- Click "Create Task" (not "Create Basic Task").
  - General tab:
    - Name: e.g., "Security Camera - On Unlock"
    - Check "Run with highest privileges".
    - Optionally select "Run whether user is logged on or not" if you want it to run in background.
  - Triggers tab:
    - Click New → Begin the task: choose one:
      - "On workstation unlock" (recommended)
      - "On workstation lock"
      - "At log on" (or "At log on of any user")
    - Click OK.
  - Actions tab:
    - Click New → Action: Start a program
      - Program/script: path to python.exe (find with `where python` in CMD or `Get-Command python` in PowerShell). Example:
        C:\Users\YourUser\AppData\Local\Programs\Python\Python312\python.exe
      - Add arguments: full path to the script and the mode argument, e.g.:
        "C:\Path\To\security_camera.py" unlock
        (Wrap the script path in quotes if it contains spaces. Replace `unlock` with `lock` or `logon` as appropriate.)
      - Start in: the script folder (optional).
    - Click OK.
  - Conditions tab:
    - Uncheck "Start the task only if the computer is on AC power" if you want it to run on battery.
  - Settings tab:
    - Optionally check "Hidden" to prevent console windows from showing.
    - Ensure "If the task fails, restart every..." is configured to your preference.
- Save. You may be prompted for credentials if you chose to run whether user is logged on or not.

- Test:
  - Lock and unlock the PC (or trigger the chosen event). Confirm email arrives.

6. Logs and file locations
- Default capture folder example: C:\SecurityCaptures
- Script logs example: C:\SecurityScript\task_debug.log or C:\SecurityCaptures\security_log.txt (check your script for exact paths).
- If you do not see photos or logs, check Task Scheduler history and the script's console output.

7. Troubleshooting
- Webcam not found: make sure the camera is enabled and not used by another program. Script tries camera indexes 0–2; if your camera uses a different index, adjust code.
- Email sending fails:
  - Verify EMAIL_SENDER, EMAIL_PASSWORD (App Password), EMAIL_RECEIVER environment variables.
  - Confirm 2‑Step Verification is enabled and App Password is active.
  - Check SMTP configuration in the script (Gmail uses smtp.gmail.com:587 with TLS).
- No photo but email sent: camera was not accessible — script still sends location-only message.
- Permission/folder errors: run a one-time test from an elevated Command Prompt or adjust folder permissions.
- Location is approximate: public IP geolocation is not precise (no GPS).

