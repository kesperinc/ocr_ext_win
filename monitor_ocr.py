import os
import time
import glob
import sys

# [AUTO] Force UTF-8 for stdout/stderr to avoid cp949 errors on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# [AUTO] Configuration
ARCHIVE_ROOT = r"d:\Archive\yukim_ocr\육임_통합"
PDF_DIR = os.path.join(ARCHIVE_ROOT, "pdf")
TXT_DIR = os.path.join(ARCHIVE_ROOT, "txt", "pdf")
LOG_DIR = r"d:\Archive\yukim_ocr\ocr_ext\logs"
LOG_PATH = os.path.join(LOG_DIR, "pdf_ocr_progress.log")
SUMMARY_LOG = os.path.join(LOG_DIR, "pdf_ocr_30min_summary.log")

TOTAL_PDFS = 2624

def get_current_stats():
    # Count files in mirrored structure using os.walk for Windows compatibility
    count = 0
    try:
        for root, dirs, files in os.walk(TXT_DIR):
            for file in files:
                if file.endswith(".md"):
                    count += 1
        return count
    except:
        return 0

def log_summary(done, remaining, delta):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{timestamp}] Done: {done}, Remaining: {remaining}, Delta(30m): {delta}"
    with open(SUMMARY_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def main():
    last_done = get_current_stats()
    log_summary(last_done, TOTAL_PDFS - last_done, 0)
    
    while True:
        time.sleep(1800) # [AUTO] 30 minutes
        current_done = get_current_stats()
        delta = current_done - last_done
        remaining = TOTAL_PDFS - current_done
        
        log_summary(current_done, remaining, delta)
        last_done = current_done

if __name__ == "__main__":
    main()
