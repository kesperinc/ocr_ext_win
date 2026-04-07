import torch
import os
import sys
import json

try:
    import docling
    from docling.document_converter import DocumentConverter
    docling_status = "Available"
except ImportError:
    docling_status = "Missing"

status = {
    "python": sys.version,
    "torch": torch.__version__,
    "cuda_available": torch.cuda.is_available(),
    "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
    "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
    "docling": docling_status
}

print(json.dumps(status, indent=2))
