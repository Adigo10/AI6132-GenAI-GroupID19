# Usage Guide

## Quick Start Guide for 360-Degree Panoramic Video Generator

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Adigo10/AI6132-GenAI-GroupID19.git
cd AI6132-GenAI-GroupID19
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### 1. Create Sample Data (Optional)

Generate sample character images for testing:
```bash
python create_samples.py
```

This creates:
- `sample_data/character_circle.png` - A circular character
- `sample_data/character_star.png` - A star-shaped character
- `sample_data/background_sky.jpg` - A simple sky background

#### 2. Run Examples

**Basic Example:**
```bash
PYTHONPATH=.:$PYTHONPATH python examples/basic_example.py
```

**Advanced Example:**
```bash
PYTHONPATH=.:$PYTHONPATH python examples/advanced_example.py
```

#### 3. Generate Your Own Video

**Using the CLI:**

Minimum required:
```bash
PYTHONPATH=.:$PYTHONPATH python main.py --character path/to/your/character.png
```

Full customization:
```bash
PYTHONPATH=.:$PYTHONPATH python main.py \
    --character path/to/character.png \
    --environment path/to/background.jpg \
    --output my_video.mp4 \
    --fps 30 \
    --num-frames 120 \
    --resolution 1920 1080 \
    --camera-radius 5.0 \
    --camera-height 10.0 \
    --character-scale 1.2
```

**Using Python API:**

```python
from panoramic_video_generator.core import (
    CharacterHandler, EnvironmentHandler, CameraTrajectory,
    SceneRenderer, VideoGenerator
)
import numpy as np

# Step 1: Load character
char_handler = CharacterHandler()
char_handler.load_character('path/to/character.png')

# Step 2: Create environment
env_handler = EnvironmentHandler()
env_handler.create_gradient_environment(
    top_color=(135, 206, 235),      # Sky blue
    bottom_color=(34, 139, 34),     # Forest green
    size=(1920, 1080)
)

# Step 3: Generate camera trajectory
camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=120)
camera.generate_circular_trajectory()

# Step 4: Render frames
renderer = SceneRenderer(output_size=(1920, 1080))
char_image, char_mask = char_handler.get_character_data()
env_image = env_handler.get_environment_data()
angles = np.linspace(0, 2 * np.pi, 120, endpoint=False)
frames = renderer.render_frames(char_image, char_mask, env_image, angles)

# Step 5: Generate video
video_gen = VideoGenerator(fps=30)
video_gen.add_frames(frames)
video_gen.generate_video('output.mp4')
```

### Configuration File

You can use a YAML configuration file for complex setups:

1. Create `my_config.yaml`:
```yaml
video:
  fps: 30
  num_frames: 120
  output_size: [1920, 1080]

camera:
  radius: 5.0
  height: 10.0

character:
  scale: 1.2

environment:
  type: gradient
  gradient_top: [135, 206, 235]
  gradient_bottom: [34, 139, 34]
```

2. Use it:
```bash
PYTHONPATH=.:$PYTHONPATH python main.py \
    --character character.png \
    --config my_config.yaml \
    --output video.mp4
```

### Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Or use the test runner:
```bash
python run_tests.py
```

### Tips and Best Practices

1. **Character Images**: Use PNG images with transparent backgrounds for best results
2. **Resolution**: Higher resolutions (1920x1080 or 4K) produce better quality but take longer
3. **Frame Count**: 
   - 60 frames = 2 seconds at 30 fps (quick demo)
   - 120 frames = 4 seconds at 30 fps (smooth rotation)
   - 180 frames = 6 seconds at 30 fps (detailed view)
4. **Camera Settings**:
   - Increase `radius` for wider shots
   - Increase `height` for more top-down perspective
   - Use `--top-view` for pure overhead rotation

### Troubleshooting

**Issue**: ModuleNotFoundError
**Solution**: Make sure to set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/project:$PYTHONPATH
```

Or install the package:
```bash
pip install -e .
```

**Issue**: Video quality is poor
**Solution**: 
- Increase resolution: `--resolution 2560 1440`
- Increase frame count: `--num-frames 180`
- Use higher quality source images

**Issue**: Character too small/large
**Solution**: Adjust character scale:
```bash
--character-scale 1.5  # Make 50% larger
--character-scale 0.7  # Make 30% smaller
```

### Advanced Features

#### Save Individual Frames
```bash
PYTHONPATH=.:$PYTHONPATH python main.py \
    --character character.png \
    --output video.mp4 \
    --output-frames frames_directory/
```

#### Use Custom Environment Color
```bash
PYTHONPATH=.:$PYTHONPATH python main.py \
    --character character.png \
    --env-type color \
    --env-color 255 192 203  # Pink background
```

#### Top-Down View
```bash
PYTHONPATH=.:$PYTHONPATH python main.py \
    --character character.png \
    --top-view
```

### Next Steps

- Experiment with different camera trajectories
- Try various environment styles
- Combine with video editing software for post-processing
- Use in presentations, social media, or educational content

### Support

For issues or questions, please open an issue on GitHub.
