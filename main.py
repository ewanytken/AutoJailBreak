from app.controller import JailBreakController
import torch
import gc

def clean_gpu_memory():

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

def main():
    JailBreakController().start()

if __name__ == "__main__":
    clean_gpu_memory()
    main()