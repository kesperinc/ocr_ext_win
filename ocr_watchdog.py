import os
import time
import subprocess
import logging
import psutil

# [AUTO] Configuration
BASE_DIR = r"d:\Archive\yukim_ocr\ocr_ext"
LOG_DIR = os.path.join(BASE_DIR, "logs")
VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
OCR_SCRIPT = "yukim_pdf_ocr.py"
WATCHDOG_LOG = os.path.join(LOG_DIR, "watchdog.log")
NOHUP_LOG = os.path.join(LOG_DIR, "pdf_ocr_restart.log")

# [AUTO] Logger setup
logging.basicConfig(
    filename=WATCHDOG_LOG,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def is_ocr_running():
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and any(OCR_SCRIPT in arg for arg in proc.info['cmdline']):
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking process: {str(e)}")
        return False

def restart_ocr():
    logging.info("OCR process not found. Restarting...")
    try:
        # Launch in background on Windows using DETACHED_PROCESS
        cmd = [VENV_PYTHON, os.path.join(BASE_DIR, OCR_SCRIPT)]
        with open(NOHUP_LOG, "a") as log_file:
            subprocess.Popen(
                cmd, 
                cwd=BASE_DIR, 
                stdout=log_file, 
                stderr=log_file, 
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        logging.info(f"Restarted OCR process: {' '.join(cmd)}")
    except Exception as e:
        logging.error(f"Failed to restart OCR: {str(e)}")

if __name__ == "__main__":
    logging.info("=== OCR Watchdog Started (30m interval) ===")
    while True:
        try:
            if not is_ocr_running():
                restart_ocr()
            else:
                logging.info("OCR process is running normally.")
        except Exception as e:
            logging.error(f"Watchdog main loop error: {str(e)}")
        
        # Sleep for 30 minutes (1800 seconds)
        time.sleep(1800)
