# AI6132-GenAI-GroupID19

## 360-Degree Panoramic Video Generator

A Gen AI project for generating 360-degree top-view panoramic videos with a character centered in a surrounding environment. The system creates smooth circular camera motions around a central character, producing professional-looking panoramic videos suitable for presentations, demonstrations, and creative projects.

## Features

- **Character-Centered Composition**: Place any character image at the center of the scene
- **Flexible Environments**: Support for image backgrounds, solid colors, or gradient environments
- **360-Degree Camera Motion**: Smooth circular or top-view camera trajectories
- **Customizable Parameters**: Full control over video resolution, FPS, camera position, and character scaling
- **Easy-to-Use API**: Both command-line and programmatic interfaces
- **High-Quality Output**: Professional video rendering with proper alpha blending

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Quick Start

### Command-Line Interface

Generate a panoramic video with a character image:

```bash
python main.py \
    --character path/to/character.png \
    --output output_video.mp4 \
    --num-frames 120 \
    --fps 30
```

### Using a Custom Environment

```bash
python main.py \
    --character path/to/character.png \
    --environment path/to/background.jpg \
    --output output_video.mp4 \
    --resolution 1920 1080
```

### Programmatic Usage

```python
from panoramic_video_generator.core import (
    CharacterHandler,
    EnvironmentHandler,
    CameraTrajectory,
    SceneRenderer,
    VideoGenerator,
)

# Load character
char_handler = CharacterHandler()
char_handler.load_character('character.png')

# Create environment
env_handler = EnvironmentHandler()
env_handler.create_gradient_environment(
    top_color=(135, 206, 235),
    bottom_color=(34, 139, 34),
    size=(1920, 1080)
)

# Generate camera trajectory
camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=120)
camera.generate_circular_trajectory()

# Render frames
renderer = SceneRenderer(output_size=(1920, 1080))
char_image, char_mask = char_handler.get_character_data()
env_image = env_handler.get_environment_data()

import numpy as np
angles = np.linspace(0, 2 * np.pi, 120, endpoint=False)
frames = renderer.render_frames(char_image, char_mask, env_image, angles)

# Generate video
video_gen = VideoGenerator(fps=30)
video_gen.add_frames(frames)
video_gen.generate_video('output.mp4')
```

## Examples

Run the included examples to see the system in action:

```bash
# Basic example with simple character
python examples/basic_example.py

# Advanced example with configuration file
python examples/advanced_example.py
```

## Project Structure

```
panoramic_video_generator/
├── core/                      # Core modules
│   ├── character_handler.py   # Character input processing
│   ├── environment_handler.py # Environment/background handling
│   ├── camera_trajectory.py   # Camera path generation
│   ├── scene_renderer.py      # Scene rendering and composition
│   └── video_generator.py     # Video output generation
├── utils/                     # Utility modules
│   ├── config.py              # Configuration management
│   └── helpers.py             # Helper functions
└── models/                    # Future: ML models for enhancement

main.py                        # Command-line interface
examples/                      # Example scripts
requirements.txt               # Python dependencies
setup.py                       # Package setup
```

## Configuration

You can use a YAML configuration file for complex setups:

```yaml
video:
  fps: 30
  num_frames: 120
  output_size: [1920, 1080]
  codec: mp4v

camera:
  radius: 5.0
  height: 10.0
  start_angle: 0.0
  trajectory_type: circular

character:
  scale: 1.0
  target_size: null

environment:
  type: gradient
  gradient_top: [135, 206, 235]
  gradient_bottom: [34, 139, 34]
```

Load configuration:

```bash
python main.py --character character.png --config config.yaml --output video.mp4
```

## Command-Line Arguments

### Input Options
- `--character`: Path to character image file (required)
- `--character-mask`: Optional path to character mask/alpha channel
- `--environment`: Path to environment/background image
- `--env-type`: Environment type (image/color/gradient)
- `--env-color`: RGB color for solid environment

### Output Options
- `--output`: Output video file path (default: output.mp4)
- `--output-frames`: Directory to save individual frames

### Video Parameters
- `--fps`: Frames per second (default: 30)
- `--num-frames`: Total frames for 360° rotation (default: 120)
- `--resolution`: Output resolution as width height (default: 1920 1080)

### Camera Parameters
- `--camera-radius`: Distance from character (default: 5.0)
- `--camera-height`: Height above scene (default: 10.0)
- `--top-view`: Use pure top-down view

### Character Parameters
- `--character-scale`: Scale factor for character (default: 1.0)

### Configuration
- `--config`: Path to YAML configuration file

## Use Cases

- **Product Demonstrations**: Showcase 3D models or products from all angles
- **Character Presentations**: Display game characters, avatars, or mascots
- **Educational Content**: Create engaging visual content for learning materials
- **Social Media**: Generate eye-catching panoramic videos for posts
- **Portfolio Showcases**: Present artistic work with dynamic camera motion

## Future Enhancements

- [ ] Integration with 3D model loading (OBJ, FBX, GLTF)
- [ ] AI-powered character extraction and segmentation
- [ ] Real-time preview and editing
- [ ] Advanced camera movements (zoom, spiral, custom paths)
- [ ] Lighting and shadow effects
- [ ] Post-processing filters and effects
- [ ] Batch processing support
- [ ] Web-based interface

## Contributing

This is a group project for AI6132. Contributions from team members are welcome!

## License

MIT License - See LICENSE file for details

## Authors

AI6132 Group 19

## Acknowledgments

- Course: AI6132 Generative AI
- Project Goal: Generate 360-degree panoramic videos with character-centered composition
Gen AI project for generating 360-degree top-view panoramic videos with character-centered circular camera motion

# Benchmarking resources
https://huggingface.co/datasets/diffusers/benchmarks
https://github.com/Schuture/Benchmarking-Awesome-Diffusion-Models
https://milvus.io/ai-quick-reference/what-are-some-common-datasets-used-to-benchmark-diffusion-models
https://arxiv.org/html/2505.11257v1
https://book.premai.io/state-of-open-source-ai/eval-datasets/
