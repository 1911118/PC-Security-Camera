# PC Security Camera Script

This Python script captures a webcam photo and sends an email alert with approximate location (via IP) on Windows events like PC unlock, lock, or logon. Useful for basic security monitoring.

## Features
- Captures photo from webcam.
- Gets approximate location from IP (city, region, etc.).
- Emails photo and details to a receiver.
- Logs events to a file.
- Runs via command line or Task Scheduler.

## Requirements
- Python 3.12+.
- Libraries: `pip install opencv-python requests`.
- Windows OS (for Task Scheduler integration).
- Gmail account for sending emails (or modify for other providers).

## Security Note
**Do not hardcode email credentials!** Use environment variables:
- Set `EMAIL_SENDER` and `EMAIL_PASSWORD` in your system environment.
- In the script, use `os.environ.get('EMAIL_SENDER')` and `os.environ.get('EMAIL_PASSWORD')`.

For Gmail: Enable 2FA and use an "App Password" from Google Account settings.

## Setup Instructions
1. Clone this repo: `git clone https://github.com/1911118/PC-Security-Camera.git`.
2. Edit `security_camera.py`:
   - Update `SAVE_FOLDER` if needed (default: C:\SecurityCaptures).
   - Set `EMAIL_RECEIVER` to your email.
   - Secure credentials as above.
3. Test: Run `python security_camera.py test` in command prompt.

## Automating with Task Scheduler
1. Open Task Scheduler.
2. Create Task:
   - Trigger: On workstation unlock/lock/log on.
   - Action: Start `python.exe` with arguments: `path\to\security_camera.py unlock` (or lock/logon).
3. Run with highest privileges.

## Usage Examples
- Manual: `python security_camera.py unlock` (captures photo and sends email).
- Events: unlock, lock, logon, test.

## Logs and Outputs
- Photos: Saved in `C:\SecurityCaptures`.
- Logs: `C:\SecurityCaptures\security_log.txt` and `C:\SecurityScript\task_debug.log`.

## Troubleshooting
- No webcam? Script skips photo but sends location.
- Email issues: Check credentials and firewall.
- Location inaccurate? It's IP-based (not GPS).

Contributions welcome! Report issues on GitHub.
