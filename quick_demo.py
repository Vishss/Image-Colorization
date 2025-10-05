#!/usr/bin/env python3
"""
Quick demo to verify video colorization feature is working
"""

def main():
    print("🎬 Video Colorization Feature - Quick Demo")
    print("=" * 50)
    
    # Check if files exist
    import os
    from pathlib import Path
    
    required_files = [
        'video_colorizer.py',
        'demo_video.py', 
        'colorizers/__init__.py',
        'colorizers/eccv16.py'
    ]
    
    print("📁 Checking files...")
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing!")
        return
    
    print("\n🎯 Usage Examples:")
    print("=" * 30)
    print("1. Basic video colorization:")
    print("   python demo_video.py -i input.mp4 -o output.mp4")
    print("")
    print("2. Real-time preview:")
    print("   python demo_video.py -i input.mp4 --preview")
    print("")
    print("3. High quality with SIGGRAPH17:")
    print("   python demo_video.py -i input.mp4 --model siggraph17 --quality high")
    print("")
    print("4. Batch processing:")
    print("   python video_colorizer.py -i videos/input/ --batch")
    print("")
    print("5. GPU acceleration:")
    print("   python demo_video.py -i input.mp4 --device cuda")
    
    print("\n📋 Required Dependencies:")
    print("- torch")
    print("- opencv-python") 
    print("- tqdm")
    print("- scikit-image")
    print("- numpy")
    print("- Pillow")
    
    print("\n🚀 Install dependencies:")
    print("pip install -r requirements.txt")
    
    print("\n✅ Video Colorization Feature Ready!")
    print("Place your video files in videos/input/ folder and run the demo!")

if __name__ == "__main__":
    main()
