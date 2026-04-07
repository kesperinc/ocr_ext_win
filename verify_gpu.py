import torch
import sys

def verify_gpu():
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if not torch.cuda.is_available():
        print("Error: CUDA is not available.")
        return False
        
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")
    
    # Try a simple computation
    try:
        print("\n--- Testing computation on GPU ---")
        x = torch.rand(100, 100).cuda()
        y = torch.rand(100, 100).cuda()
        z = torch.matmul(x, y)
        print("Success: Tensor multiplication on GPU completed.")
        
        # Check compute capability
        props = torch.cuda.get_device_properties(0)
        print(f"Compute capability: {props.major}.{props.minor}")
        
        return True
    except Exception as e:
        print(f"Error during GPU computation: {str(e)}")
        return False

if __name__ == "__main__":
    success = verify_gpu()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
