<!--<h3><b>Colorful Image Colorization</b></h3>-->
## <b>Colorful Image Colorization</b> [[Project Page]](http://richzhang.github.io/colorization/) <br>
[Richard Zhang](https://richzhang.github.io/), [Phillip Isola](http://web.mit.edu/phillipi/), [Alexei A. Efros](http://www.eecs.berkeley.edu/~efros/). In [ECCV, 2016](http://arxiv.org/pdf/1603.08511.pdf).

**+ automatic colorization functionality for Real-Time User-Guided Image Colorization with Learned Deep Priors, SIGGRAPH 2017!**

**🎬 NEW: Video Colorization Feature!** Transform black and white videos into colorful ones!

**[Sept20 Update]** Since it has been 3-4 years, I converted this repo to support minimal test-time usage in PyTorch. I also added our SIGGRAPH 2017 (it's an interactive method but can also do automatic). See the [Caffe branch](https://github.com/richzhang/colorization/tree/caffe) for the original release.

![Teaser Image](http://richzhang.github.io/colorization/resources/images/teaser4.jpg)

## 🚀 Quick Start

**Clone the repository; install dependencies**

```bash
git clone https://github.com/richzhang/colorization.git
pip install -r requirements.txt
```

**Colorize Images!** This script will colorize an image. The results should match the images in the `imgs_out` folder.

```bash
python demo_release.py -i imgs/ansel_adams3.jpg
```

**🎬 Colorize Videos!** Transform black and white videos into colorful ones:

```bash
# Basic video colorization
python demo_video.py -i path/to/video.mp4 -o colorized_video.mp4

# Real-time preview
python demo_video.py -i path/to/video.mp4 --preview

# High quality with SIGGRAPH17 model
python demo_video.py -i path/to/video.mp4 --model siggraph17 --quality high
```

## 🎥 Video Colorization Features

- 🎬 **Full video processing** - Colorize entire video files
- ⚡ **Real-time preview** - See results as you process
- 🎛️ **Quality control** - Low, medium, high quality options
- 🚀 **GPU acceleration** - CUDA support for faster processing
- 📊 **Progress tracking** - Visual progress bars
- 🎨 **Multiple models** - ECCV16 and SIGGRAPH17 support
- 📁 **Batch processing** - Process multiple videos at once

### Video Usage Examples

```bash
# Simple colorization
python demo_video.py -i videos/input/sample.mp4

# Batch process directory
python video_colorizer.py -i videos/input/ -o videos/output/ --batch

# GPU accelerated high quality
python demo_video.py -i sample.mp4 --device cuda --quality high

# Frame skipping for speed
python demo_video.py -i sample.mp4 --frame_skip 2
```

### Supported Video Formats
- **Input**: MP4, AVI, MOV, MKV, WMV
- **Output**: MP4 (H.264)

**Model loading in Python** The following loads pretrained colorizers. See [demo_release.py](demo_release.py) for some details on how to run the model. There are some pre and post-processing steps: convert to Lab space, resize to 256x256, colorize, and concatenate to the original full resolution, and convert to RGB.

```python
import colorizers
colorizer_eccv16 = colorizers.eccv16().eval()
colorizer_siggraph17 = colorizers.siggraph17().eval()
```

### Original implementation (Caffe branch)

The original implementation contained train and testing, our network and AlexNet (for representation learning tests), as well as representation learning tests. It is in Caffe and is no longer supported. Please see the [caffe](https://github.com/richzhang/colorization/tree/caffe) branch for it.

### Citation ###

If you find these models useful for your resesarch, please cite with these bibtexs.

```
@inproceedings{zhang2016colorful,
  title={Colorful Image Colorization},
  author={Zhang, Richard and Isola, Phillip and Efros, Alexei A},
  booktitle={ECCV},
  year={2016}
}

@article{zhang2017real,
  title={Real-Time User-Guided Image Colorization with Learned Deep Priors},
  author={Zhang, Richard and Zhu, Jun-Yan and Isola, Phillip and Geng, Xinyang and Lin, Angela S and Yu, Tianhe and Efros, Alexei A},
  journal={ACM Transactions on Graphics (TOG)},
  volume={9},
  number={4},
  year={2017},
  publisher={ACM}
}
```

### Misc ###
Contact Richard Zhang at rich.zhang at eecs.berkeley.edu for any questions or comments.



### running Command
python demo_release.py -i imgs/tree.jpg -o imgs_out/tree
