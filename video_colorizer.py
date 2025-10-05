import cv2
import numpy as np
import torch
import argparse
from pathlib import Path
from tqdm import tqdm
import tempfile
import os
from colorizers import *
from colorizers.util import preprocess_img, postprocess_tens

class VideoColorizer:
    def __init__(self, model_type='eccv16', device='cpu'):
        """
        Initialize video colorizer
        Args:
            model_type: 'eccv16' or 'siggraph17'
            device: 'cpu' or 'cuda'
        """
        self.device = device
        self.model_type = model_type
        self.colorizer = self._load_model()
        
    def _load_model(self):
        """Load the colorization model"""
        if self.model_type == 'eccv16':
            model = eccv16(pretrained=True)
        else:
            model = siggraph17(pretrained=True)
        
        model.eval()
        if self.device == 'cuda' and torch.cuda.is_available():
            model = model.cuda()
        return model
    
    def colorize_frame(self, frame):
        """
        Colorize a single frame
        Args:
            frame: BGR frame from OpenCV
        Returns:
            colorized_frame: BGR colorized frame
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Preprocess
        (tens_l_orig, tens_l_rs) = preprocess_img(frame_rgb, HW=(256,256))
        
        if self.device == 'cuda' and torch.cuda.is_available():
            tens_l_rs = tens_l_rs.cuda()
        
        # Colorize
        with torch.no_grad():
            out_ab = self.colorizer(tens_l_rs).cpu()
        
        # Postprocess
        colorized_rgb = postprocess_tens(tens_l_orig, out_ab)
        
        # Convert RGB back to BGR
        colorized_bgr = cv2.cvtColor((colorized_rgb * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        
        return colorized_bgr
    
    def colorize_video(self, input_path, output_path, frame_skip=1, quality='medium'):
        """
        Colorize entire video
        Args:
            input_path: Path to input video
            output_path: Path to output video
            frame_skip: Process every nth frame (1 = all frames)
            quality: 'low', 'medium', 'high'
        """
        cap = cv2.VideoCapture(str(input_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Quality settings
        quality_settings = {
            'low': {'crf': 28, 'preset': 'fast'},
            'medium': {'crf': 23, 'preset': 'medium'},
            'high': {'crf': 18, 'preset': 'slow'}
        }
        
        # Setup temporary output for high quality encoding
        temp_output = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_path = temp_output.name
        temp_output.close()
        
        # Video writer for temporary file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_path, fourcc, fps//frame_skip, (width, height))
        
        frame_count = 0
        processed_frames = 0
        
        print(f"Processing {total_frames//frame_skip} frames...")
        print(f"Model: {self.model_type}, Device: {self.device}")
        print(f"Video specs: {width}x{height} @ {fps}fps")
        
        with tqdm(total=total_frames//frame_skip, desc="Colorizing", unit="frames") as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_skip == 0:
                    # Colorize frame
                    colorized_frame = self.colorize_frame(frame)
                    out.write(colorized_frame)
                    processed_frames += 1
                    pbar.update(1)
                
                frame_count += 1
        
        cap.release()
        out.release()
        
        # Re-encode with better quality using ffmpeg if available
        try:
            import subprocess
            quality_opts = quality_settings[quality]
            cmd = [
                'ffmpeg', '-i', temp_path, '-c:v', 'libx264',
                '-crf', str(quality_opts['crf']),
                '-preset', quality_opts['preset'],
                '-y', str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            os.unlink(temp_path)  # Remove temporary file
            print(f"✅ Video saved to: {output_path}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: just rename temp file
            os.rename(temp_path, str(output_path))
            print(f"✅ Video saved to: {output_path} (basic quality)")
    
    def colorize_video_realtime(self, input_path, show_preview=True):
        """
        Real-time video colorization with preview
        """
        cap = cv2.VideoCapture(str(input_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")
        
        print("🎬 Real-time Video Colorization")
        print("Press 'q' to quit, 'p' to pause/resume")
        
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("End of video reached")
                    break
                
                # Colorize frame
                colorized_frame = self.colorize_frame(frame)
                
                if show_preview:
                    # Show side-by-side comparison
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
                    
                    # Resize for display
                    h, w = frame.shape[:2]
                    display_h, display_w = 480, 640
                    gray_frame = cv2.resize(gray_frame, (display_w//2, display_h))
                    colorized_frame = cv2.resize(colorized_frame, (display_w//2, display_h))
                    
                    # Combine frames
                    combined = np.hstack([gray_frame, colorized_frame])
                    cv2.putText(combined, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    cv2.putText(combined, "Colorized", (display_w//2 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    cv2.putText(combined, "Press 'q' to quit, 'p' to pause", (10, display_h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                    
                    cv2.imshow('Video Colorization', combined)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = not paused
                print("⏸️ Paused" if paused else "▶️ Resumed")
        
        cap.release()
        cv2.destroyAllWindows()
    
    def batch_colorize_videos(self, input_dir, output_dir, **kwargs):
        """
        Colorize all videos in a directory
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(input_path.glob(f'*{ext}'))
            video_files.extend(input_path.glob(f'*{ext.upper()}'))
        
        print(f"Found {len(video_files)} video files")
        
        for video_file in video_files:
            output_file = output_path / f"colorized_{video_file.name}"
            print(f"\n🎬 Processing: {video_file.name}")
            
            try:
                self.colorize_video(video_file, output_file, **kwargs)
            except Exception as e:
                print(f"❌ Error processing {video_file.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Video Colorization')
    parser.add_argument('-i', '--input', required=True, help='Input video path or directory')
    parser.add_argument('-o', '--output', help='Output video path or directory')
    parser.add_argument('--model', choices=['eccv16', 'siggraph17'], default='eccv16', help='Model type')
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu', help='Device to use')
    parser.add_argument('--frame_skip', type=int, default=1, help='Process every nth frame')
    parser.add_argument('--quality', choices=['low', 'medium', 'high'], default='medium', help='Output quality')
    parser.add_argument('--realtime', action='store_true', help='Real-time preview mode')
    parser.add_argument('--batch', action='store_true', help='Batch process directory of videos')
    
    args = parser.parse_args()
    
    print("🎨 Video Colorization Tool")
    print("=" * 50)
    
    colorizer = VideoColorizer(model_type=args.model, device=args.device)
    
    if args.realtime:
        colorizer.colorize_video_realtime(args.input)
    elif args.batch:
        if not args.output:
            args.output = str(Path(args.input).parent / "colorized_videos")
        colorizer.batch_colorize_videos(
            args.input, 
            args.output,
            frame_skip=args.frame_skip,
            quality=args.quality
        )
    else:
        if not args.output:
            input_path = Path(args.input)
            args.output = input_path.parent / f"colorized_{input_path.name}"
        
        colorizer.colorize_video(
            args.input, 
            args.output, 
            frame_skip=args.frame_skip,
            quality=args.quality
        )

if __name__ == "__main__":
    main()
