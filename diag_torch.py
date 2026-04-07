import torch
import torchvision
import transformers
from transformers.utils import is_torch_available, is_torchvision_available
import sys
import os

print(f"Python Executeable: {sys.executable}")
print(f"Python path: {sys.path}")
print(f"Torch version: {torch.__version__}")
print(f"Torchvision version: {torchvision.__version__}")
print(f"Transformers version: {transformers.__version__}")

print(f"Is Torch available to Transformers? {is_torch_available()}")
print(f"Is Torchvision available to Transformers? {is_torchvision_available()}")

# Force check logic
try:
    import torch
    import torchvision
    print("Direct imports successful")
except Exception as e:
    print(f"Direct import failed: {e}")

# Check for specific dependency that triggers the failure
try:
    from transformers.utils.import_utils import _is_package_available
    print(f"Package 'torch' available via import_utils: {_is_package_available('torch')}")
except Exception as e:
    print(f"Import utils failed: {e}")
