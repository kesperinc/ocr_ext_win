import os
import glob
import time
import json
import sys

# [AUTO] Force UTF-8 for stdout/stderr to avoid cp949 errors on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# [AUTO] Toggle GPU/CPU usage
USE_GPU = False  # True면 GPU(CUDA), False면 CPU 사용

# [AUTO] Strict Resource Limits (Stability over Speed)
# 이 설정들은 Docling/PyTorch가 모든 CPU 코어를 점유하여 시스템이 다운되는 것을 방지합니다.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

if USE_GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ["DOCLING_DEVICE"] = "cuda"
else:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["DOCLING_DEVICE"] = "cpu"

# [AUTO] Deferred Imports for visibility
import torch # GPU 캐시 관리를 위해 추가
InputFormat = None
PdfPipelineOptions = None
DocumentConverter = None
PdfFormatOption = None

# [AUTO] Configuration
ARCHIVE_ROOT = r"d:\Archive\yukim_ocr\육임_통합"
PDF_DIR = os.path.join(ARCHIVE_ROOT, "pdf")
TXT_DIR = os.path.join(ARCHIVE_ROOT, "txt", "pdf")
os.makedirs(TXT_DIR, exist_ok=True)

# [AUTO] File management
LOG_DIR = r"d:\Archive\yukim_ocr\ocr_ext\logs"
LOG_PATH = os.path.join(LOG_DIR, "pdf_ocr_progress.log")
FAIL_TRACKER_PATH = os.path.join(LOG_DIR, "fail_tracker.json")
PERMANENT_FAIL_LOG = os.path.join(LOG_DIR, "pdf_ocr_failed_permanent.log")

def log_progress(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    print(msg)

def log_permanent_fail(msg):
    with open(PERMANENT_FAIL_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_fail_tracker():
    if os.path.exists(FAIL_TRACKER_PATH):
        try:
            with open(FAIL_TRACKER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_fail_tracker(tracker):
    with open(FAIL_TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(tracker, f)

# [AUTO] Scan PDFs
log_progress("Searching for PDF files in ARCHIVE_ROOT...")
pdf_files = glob.glob(f"{PDF_DIR}/**/*.pdf", recursive=True)
total_count = len(pdf_files)
log_progress(f"=== Total PDF files to process: {total_count} ===")

# [AUTO] Heavy imports start here
log_progress("Initializing OCR models (Docling/Torch)...")
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
log_progress("Models loaded. Configuring pipeline...")

pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options.num_threads = 1 # [AUTO] Core limit
pipeline_options.accelerator_options.device = "cuda" if USE_GPU else "cpu"

# [AUTO] Limit batch sizes to prevent OOM/CPU spikes
pipeline_options.ocr_options.batch_size = 1
# pipeline_options.layout_options.batch_size = 1 # docling 버전에 따라 다를 수 있음

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

completed_count = 0
fail_tracker = load_fail_tracker()

for pdf_path in pdf_files:
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(TXT_DIR, f"{base_name}.md")
    
    if os.path.exists(output_path):
        log_progress(f"[Skip] {base_name} - Already exists.")
        completed_count += 1
        continue
    
    # [AUTO] Check failure history (Skip if failed >= 2 times)
    current_fails = fail_tracker.get(pdf_path, 0)
    if current_fails >= 2:
        log_progress(f"[PERMANENT SKIP] {base_name} - Failed {current_fails} times.")
        log_permanent_fail(f"{pdf_path} (Failed {current_fails} times)")
        completed_count += 1
        continue

    try:
        # [AUTO] Log processing and increment failure count before starting
        log_progress(f"[Convert] {base_name} ({completed_count + 1}/{total_count})...")
        fail_tracker[pdf_path] = current_fails + 1
        save_fail_tracker(fail_tracker)

        result = converter.convert(pdf_path)
        
        # [AUTO] Export to Markdown (Recommended for LLM indexing)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.document.export_to_markdown())
            
        log_progress(f"[DONE] {base_name} saved.")
        
        # [AUTO] Success! Remove from failure tracker
        if pdf_path in fail_tracker:
            del fail_tracker[pdf_path]
            save_fail_tracker(fail_tracker)

    except Exception as e:
        log_progress(f"[Error] Failed to convert {base_name}: {str(e)}")
        # Check if it was a memory error or hard crash (implicitly handled by count in JSON)
        # Note: failure count remains in JSON for next run
    
    finally:
        # [AUTO] Force cleanup after every document to maintain system stability
        if USE_GPU and torch.cuda.is_available():
            torch.cuda.empty_cache()
            # print("DEBUG: GPU Cache cleared.")
        
    completed_count += 1

log_progress("All PDF OCR tasks completed.")
