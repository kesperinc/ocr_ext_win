import time
import os
from docling.document_converter import DocumentConverter

PDF_PATH = "/mnt/d/Archive/육임_통합/pdf/01 북해한인 - 육임금침.pdf"
print(f"Starting conversion for: {PDF_PATH}")

try:
    start = time.time()
    converter = DocumentConverter()
    print("Converter initialized.")
    
    result = converter.convert(PDF_PATH)
    print("Conversion finished.")
    
    output_path = "test_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())
    
    print(f"Success! Saved to {output_path} in {time.time()-start:.2f}s")
except Exception as e:
    print(f"Error during conversion: {str(e)}")
