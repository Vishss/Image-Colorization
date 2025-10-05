#!/usr/bin/env python3
"""
Video Colorization Demo Script
Usage: python demo_video.py -i input_video.mp4 -o output_video.mp4
"""

from video_colorizer import VideoColorizer
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Colorize video files')
    parser.add_argument('-i', '--input', required=True, help='Input video file')
    parser.add_argument('-o', '--output', help='Output video file (optional)')
    parser.add_argument('--model', choices=['eccv16', 'siggraph17'], default='eccv16', 
                       help='Choose colorization model (default: eccv16)')
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu',
                       help='Device to use for processing (default: cpu)')
    parser.add_argument('--quality', choices=['low', 'medium', 'high'], default='medium',
                       help='Output video quality (default: medium)')
    parser.add_argument('--frame_skip', type=int, default=1, 
                       help='Process every nth frame (default: 1)')
    parser.add_argument('--preview', action='store_true', 
                       help='Show real-time preview instead of saving')
    
    args = parser.parse_args()
    
    # Auto-generate output filename if not provided
    if not args.output and not args.preview:
        input_path = Path(args.input)
        args.output = input_path.parent / f"colorized_{input_path.name}"
    
    print("🎬 Video Colorization Demo")
    print("=" * 40)
    print(f"📁 Input: {args.input}")
    if not args.preview:
        print(f"💾 Output: {args.output}")
    print(f"🤖 Model: {args.model}")
    print(f"⚙️  Device: {args.device}")
    print(f"🎯 Quality: {args.quality}")
    print("=" * 40)
    
    try:
        # Initialize colorizer
        colorizer = VideoColorizer(model_type=args.model, device=args.device)
        
        if args.preview:
            print("🔴 Starting real-time preview mode...")
            print("Press 'q' to quit, 'p' to pause/resume")
            colorizer.colorize_video_realtime(args.input)
        else:
            print("🎨 Starting video colorization...")
            colorizer.colorize_video(
                args.input, 
                args.output, 
                frame_skip=args.frame_skip,
                quality=args.quality
            )
            print("✅ Video colorization completed successfully!")
            print(f"📁 Output saved to: {args.output}")
        
    except FileNotFoundError:
        print("❌ Error: Input video file not found!")
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        print("💡 Tip: Try using --device cpu if you're having GPU issues")

if __name__ == "__main__":
    main()
