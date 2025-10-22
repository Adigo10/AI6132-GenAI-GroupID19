# Project Documentation

## 360-Degree Panoramic Video Generator - AI6132 Group 19

### Project Overview

This is a Gen AI project that generates 360-degree top-view panoramic videos featuring a character centered in a surrounding environment. The system creates smooth circular camera motions around the central character, producing professional-looking panoramic videos.

### Key Features

1. **Character-Centered Composition**
   - Supports PNG images with alpha/transparency
   - Automatic character positioning at scene center
   - Adjustable character scaling

2. **Flexible Environment System**
   - Image-based backgrounds
   - Solid color backgrounds
   - Gradient backgrounds (vertical)
   - Custom RGB color support

3. **Advanced Camera System**
   - Circular trajectory around character
   - Top-down view with rotation
   - Configurable camera radius and height
   - Smooth 360-degree motion

4. **Professional Video Output**
   - High-quality video rendering
   - Customizable resolution (720p, 1080p, 4K)
   - Adjustable frame rate (FPS)
   - MP4 video format with OpenCV
   - Optional MoviePy support for enhanced formats

### Architecture

```
panoramic_video_generator/
├── core/                       # Core functionality
│   ├── character_handler.py    # Character loading & preprocessing
│   ├── environment_handler.py  # Environment creation & management
│   ├── camera_trajectory.py    # Camera path generation
│   ├── scene_renderer.py       # Frame rendering & composition
│   └── video_generator.py      # Video file generation
├── utils/                      # Utility modules
│   ├── config.py               # Configuration management
│   └── helpers.py              # Helper functions
└── models/                     # Future ML models (placeholder)
```

### Technical Implementation

#### 1. Character Handler (`character_handler.py`)
- Loads character images (PNG, JPEG)
- Handles alpha channels and transparency
- Automatic mask generation
- Image preprocessing and scaling

#### 2. Environment Handler (`environment_handler.py`)
- Three environment types: image, color, gradient
- Flexible sizing and scaling
- RGB color space support

#### 3. Camera Trajectory (`camera_trajectory.py`)
- Circular path generation using parametric equations
- Configurable radius and height
- Frame-by-frame camera parameters
- Support for both circular and top-view trajectories

#### 4. Scene Renderer (`scene_renderer.py`)
- Alpha blending for character composition
- Real-time frame rendering
- Character rotation based on camera angle
- Efficient memory management

#### 5. Video Generator (`video_generator.py`)
- OpenCV-based video encoding
- Optional MoviePy support
- Frame-by-frame video construction
- Progress tracking with tqdm

### Usage Modes

#### 1. Command-Line Interface (CLI)
```bash
python main.py --character char.png --output video.mp4
```

#### 2. Python API
```python
from panoramic_video_generator.core import *
# ... detailed API usage
```

#### 3. Configuration File
```yaml
video:
  fps: 30
  num_frames: 120
# ... YAML configuration
```

### Testing

Comprehensive test suite with 21 unit tests covering:
- Character loading and preprocessing
- Environment creation (all types)
- Camera trajectory generation
- Scene rendering
- Video generation
- Configuration management

Test coverage: All core modules tested
Test framework: pytest

### Performance Characteristics

- **Memory Usage**: Moderate (frames are generated on-demand)
- **Processing Speed**: 
  - 60 frames: ~1-2 seconds on modern hardware
  - 120 frames: ~3-4 seconds on modern hardware
- **Video Quality**: High (lossless PNG to MP4 conversion)
- **Scalability**: Handles resolutions up to 4K

### Dependencies

Core:
- numpy: Numerical operations
- opencv-python: Image processing & video encoding
- pillow: Image loading and manipulation
- scipy: Scientific computing utilities
- tqdm: Progress bars

Optional:
- moviepy: Enhanced video generation
- torch/torchvision: Future ML enhancements
- trimesh/pyrender: Future 3D rendering

### Future Enhancements

Planned features:
1. **3D Model Support**: Import OBJ, FBX, GLTF models
2. **AI-Powered Features**:
   - Automatic character extraction
   - Background generation with diffusion models
   - Style transfer
3. **Advanced Camera Movements**:
   - Spiral trajectories
   - Zoom effects
   - Custom path definitions
4. **Rendering Improvements**:
   - Lighting and shadows
   - Reflections
   - Post-processing effects
5. **User Interface**:
   - Web-based interface
   - Real-time preview
   - Interactive editing

### Development Guidelines

1. **Code Style**: Follow PEP 8
2. **Testing**: Write tests for new features
3. **Documentation**: Update docs with changes
4. **Version Control**: Use meaningful commit messages
5. **Performance**: Profile before optimization

### Known Limitations

1. **2D Only**: Currently supports only 2D images, not 3D models
2. **Single Character**: One character per video
3. **Fixed Camera Path**: Limited to circular and top-view trajectories
4. **No Audio**: Video generation without audio support (can be added via MoviePy)
5. **Static Environment**: Background doesn't change during rotation

### Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **OS**: Linux, macOS, Windows
- **Hardware**: CPU-based (no GPU required, but beneficial for future features)

### License

MIT License - See LICENSE file

### Authors

AI6132 Group 19
Course: AI6132 Generative AI

### Acknowledgments

- NumPy and SciPy communities
- OpenCV project
- PIL/Pillow team
- pytest framework

### Citation

If you use this project in your research or work, please cite:

```
AI6132 Group 19. (2025). 360-Degree Panoramic Video Generator.
https://github.com/Adigo10/AI6132-GenAI-GroupID19
```

### Contact

For questions, issues, or contributions, please:
1. Open an issue on GitHub
2. Submit a pull request
3. Contact the course instructors

---

**Last Updated**: October 2025
**Version**: 0.1.0
**Status**: Production Ready
