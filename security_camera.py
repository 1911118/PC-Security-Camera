import cv2
import smtplib
import ssl
import os
import requests
import json
from datetime import datetime
from email.message import EmailMessage
import sys
import time

# ADD AT THE VERY BEGINNING OF YOUR SCRIPT
import sys
import os
from datetime import datetime

# Create debug log
debug_log = r"C:\SecurityScript\task_debug.log"

def debug_log_message(message):
    with open(debug_log, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

# Log script start
debug_log_message(f"Script started by Task Scheduler")
debug_log_message(f"Arguments: {sys.argv}")
debug_log_message(f"User: {os.getlogin()}")
debug_log_message(f"Current dir: {os.getcwd()}")
# === CONFIGURATION ===
SAVE_FOLDER = r"C:\SecurityCaptures"
EMAIL_SENDER = "send@gmail.com"
EMAIL_PASSWORD = "app password "  # Keep this secure!
EMAIL_RECEIVER = "recever@gmail.com"

# CREATE FOLDERS IF THEY DON'T EXIST
def setup_folders():
    """Create necessary folders if they don't exist"""
    folders = [SAVE_FOLDER, r"C:\SecurityScript"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
    return True

def get_location():
    """Try to get approximate location from IP address"""
    try:
        # Using free IP location service (less accurate than GPS)
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        location = f"Approximate Location: {data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}\n"
        location += f"IP: {data.get('ip', 'Unknown')}\nCoordinates: {data.get('loc', 'Unknown')}"
        return location
    except Exception as e:
        return f"Location unavailable: {str(e)}"

def capture_photo():
    """Capture photo from webcam"""
    try:
        time.sleep(2)  # Wait for camera to initialize
        
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)
        
        # Try different camera indexes
        for i in range(3):
            cam = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cam.isOpened():
                # Read a few frames to adjust lighting
                for _ in range(5):
                    ret, frame = cam.read()
                cam.release()
                
                if ret and frame is not None:
                    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
                    filepath = os.path.join(SAVE_FOLDER, filename)
                    cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    print(f"Photo captured: {filename}")
                    return filepath
            cam.release()
            time.sleep(0.5)
        
        print("ERROR: Could not open any webcam")
        return None
    except Exception as e:
        log(f"Camera error: {str(e)}")
        return None

def send_email(filepath, event_type):
    """Send email with photo and location"""
    try:
        location_info = get_location()
        
        msg = EmailMessage()
        msg["Subject"] = f"PC Security Alert: {event_type} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        
        # Email body with location
        msg.set_content(f"Security event detected: {event_type}\n\n{location_info}\n\nTime: {datetime.now()}")
        
        # Attach photo if available
        if filepath and os.path.exists(filepath):
            with open(filepath, "rb") as f:
                img_data = f.read()
            msg.add_attachment(img_data, maintype="image", subtype="jpeg", 
                             filename=os.path.basename(filepath))
        else:
            msg.set_content(f"Security event detected: {event_type}\n\n{location_info}\n\nTime: {datetime.now()}\n\nNo photo captured - camera may be unavailable.")
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        log(f"Email sent for {event_type} event")
        print(f"Email sent successfully for {event_type}")
        return True
    except Exception as e:
        log(f"Email failed: {str(e)}")
        print(f"Email failed: {str(e)}")
        return False

def log(message):
    """Log events to file"""
    try:
        log_path = os.path.join(SAVE_FOLDER, "security_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        print(f"Logged: {message}")
    except Exception as e:
        print(f"Logging failed: {str(e)}")

if __name__ == "__main__":
    # Step 1: Create folders first
    setup_folders()
    
    # Step 2: Determine event type
    event_type = sys.argv[1] if len(sys.argv) > 1 else "test"
    
    print(f"=== Security Script Started ===")
    print(f"Event type: {event_type}")
    print(f"Save folder: {SAVE_FOLDER}")
    
    # Step 3: Capture photo for supported events
    photo_path = None
    if event_type.lower() in ["unlock", "lock", "logon", "test"]:
        photo_path = capture_photo()
    
    # Step 4: Send email with location info
    if photo_path or event_type.lower() in ["unlock", "lock", "logon", "test"]:
        send_email(photo_path, event_type)
    
    print(f"=== Script Completed ===")
    time.sleep(2)  # Keep window open to see output
