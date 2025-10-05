#!/usr/bin/env python3
"""
Test script for video colorization feature
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
    except ImportError:
        print("❌ PyTorch not found - install with: pip install torch")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError:
        print("❌ OpenCV not found - install with: pip install opencv-python")
        return False
    
    try:
        from colorizers import eccv16, siggraph17
        print("✅ Colorizers imported successfully")
    except ImportError:
        print("❌ Colorizers module not found")
        return False
    
    try:
        from video_colorizer import VideoColorizer
        print("✅ VideoColorizer imported successfully")
    except ImportError:
        print("❌ VideoColorizer not found - check if video_colorizer.py exists")
        return False
    
    return True

def test_models():
    """Test if models can be loaded"""
    print("\n🤖 Testing model loading...")
    
    try:
        from colorizers import eccv16, siggraph17
        
        # Test ECCV16
        model_eccv = eccv16(pretrained=True)
        model_eccv.eval()
        print("✅ ECCV16 model loaded successfully")
        
        # Test SIGGRAPH17
        model_sigg = siggraph17(pretrained=True)
        model_sigg.eval()
        print("✅ SIGGRAPH17 model loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_video_colorizer():
    """Test VideoColorizer initialization"""
    print("\n🎬 Testing VideoColorizer...")
    
    try:
        from video_colorizer import VideoColorizer
        
        # Test CPU initialization
        colorizer_cpu = VideoColorizer(model_type='eccv16', device='cpu')
        print("✅ VideoColorizer (CPU) initialized successfully")
        
        # Test CUDA if available
        import torch
        if torch.cuda.is_available():
            colorizer_gpu = VideoColorizer(model_type='eccv16', device='cuda')
            print("✅ VideoColorizer (CUDA) initialized successfully")
        else:
            print("ℹ️  CUDA not available, skipping GPU test")
        
        return True
    except Exception as e:
        print(f"❌ VideoColorizer initialization failed: {e}")
        return False

def check_project_structure():
    """Check if all required files exist"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'video_colorizer.py',
        'demo_video.py',
        'requirements.txt',
        'colorizers/__init__.py',
        'colorizers/eccv16.py',
        'colorizers/siggraph17.py',
        'colorizers/util.py',
        'videos/README.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_exist = False
    
    return all_exist

def main():
    print("🎨 Video Colorization Feature Test")
    print("=" * 50)
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Project structure incomplete!")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed!")
        return False
    
    # Test models
    if not test_models():
        print("\n❌ Model test failed!")
        return False
    
    # Test VideoColorizer
    if not test_video_colorizer():
        print("\n❌ VideoColorizer test failed!")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Video colorization feature is ready!")
    print("\n📖 Usage examples:")
    print("   python demo_video.py -i input.mp4 --preview")
    print("   python demo_video.py -i input.mp4 -o output.mp4")
    print("   python video_colorizer.py -i input_dir/ --batch")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
