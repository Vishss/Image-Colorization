# 🎬 Video Colorization Examples

## Basic Usage

**Simple video colorization:**
```bash
python demo_video.py -i videos/input/sample.mp4 -o videos/output/colorized_sample.mp4
```

**Real-time preview:**
```bash
python demo_video.py -i videos/input/sample.mp4 --preview
```

**High quality with SIGGRAPH17 model:**
```bash
python demo_video.py -i videos/input/sample.mp4 --model siggraph17 --quality high
```

## Advanced Usage

**Batch processing:**
```bash
python video_colorizer.py -i videos/input/ -o videos/output/ --batch
```

**GPU acceleration:**
```bash
python demo_video.py -i videos/input/sample.mp4 --device cuda
```

**Frame skipping for faster processing:**
```bash
python demo_video.py -i videos/input/sample.mp4 --frame_skip 2
```

## Command Reference

### demo_video.py (Simple Interface)
- `-i, --input`: Input video file (required)
- `-o, --output`: Output video file (optional, auto-generated if not provided)
- `--model`: Choose model (eccv16 or siggraph17)
- `--device`: Processing device (cpu or cuda)
- `--quality`: Output quality (low, medium, high)
- `--frame_skip`: Process every nth frame
- `--preview`: Real-time preview mode

### video_colorizer.py (Advanced Interface)
- All demo_video.py options plus:
- `--batch`: Batch process directory of videos
- `--realtime`: Real-time processing with controls

## Tips

1. **For faster processing**: Use `--frame_skip 2` or higher
2. **For better quality**: Use `--model siggraph17 --quality high`
3. **For GPU acceleration**: Ensure CUDA is available and use `--device cuda`
4. **For preview**: Use `--preview` to see results before processing full video

## Supported Formats

**Input**: MP4, AVI, MOV, MKV, WMV
**Output**: MP4 (H.264)

Place your input videos in the `videos/input/` folder and outputs will be saved to `videos/output/`.
