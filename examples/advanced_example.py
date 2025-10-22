#!/usr/bin/env python3
"""
Advanced example demonstrating configuration file usage and top-view mode.
"""

import numpy as np
from PIL import Image
import os

from panoramic_video_generator.core import (
    CharacterHandler,
    EnvironmentHandler,
    CameraTrajectory,
    SceneRenderer,
    VideoGenerator,
)
from panoramic_video_generator.utils import Config


def create_complex_character():
    """Create a more complex sample character for demonstration."""
    size = 300
    img = np.ones((size, size, 4), dtype=np.uint8) * 255
    img[:, :, 3] = 0  # Transparent background
    
    # Draw a stylized character (star shape)
    center = size // 2
    points = []
    for i in range(10):
        angle = i * np.pi / 5
        r = size // 3 if i % 2 == 0 else size // 6
        x = int(center + r * np.cos(angle - np.pi/2))
        y = int(center + r * np.sin(angle - np.pi/2))
        points.append([x, y])
    
    # Fill the star
    import cv2
    points = np.array(points, dtype=np.int32)
    cv2.fillPoly(img, [points], (255, 215, 0, 255))  # Gold color
    
    mask = img[:, :, 3]
    return img, mask


def main():
    """Main example function."""
    print("=" * 60)
    print("Advanced Panoramic Video Generation Example")
    print("=" * 60)
    
    # Load or create configuration
    config = Config()
    config.set('video.fps', 30)
    config.set('video.num_frames', 90)
    config.set('video.output_size', [1280, 720])
    config.set('camera.radius', 7.0)
    config.set('camera.height', 12.0)
    
    # Save configuration for reference
    os.makedirs("examples", exist_ok=True)
    config.save_yaml("examples/config_advanced.yaml")
    print("\n✓ Configuration saved to examples/config_advanced.yaml")
    
    num_frames = config.get('video.num_frames')
    fps = config.get('video.fps')
    output_size = tuple(config.get('video.output_size'))
    output_file = "examples/output_advanced.mp4"
    
    # Step 1: Create complex character
    print("\n[1/5] Creating complex character...")
    char_handler = CharacterHandler()
    char_img, char_mask = create_complex_character()
    char_handler.load_character_from_array(char_img, char_mask)
    print("  ✓ Complex character created (star shape)")
    
    # Step 2: Create environment with custom colors
    print("\n[2/5] Creating custom environment...")
    env_handler = EnvironmentHandler()
    env_handler.create_gradient_environment(
        top_color=(25, 25, 112),    # Midnight blue
        bottom_color=(75, 0, 130),  # Indigo
        size=output_size
    )
    print("  ✓ Custom gradient environment created")
    
    # Step 3: Generate top-view trajectory
    print("\n[3/5] Generating top-view camera trajectory...")
    camera = CameraTrajectory(
        radius=config.get('camera.radius'),
        height=config.get('camera.height'),
        num_frames=num_frames
    )
    camera.generate_top_view_trajectory(center=(0, 0, 0))
    print(f"  ✓ Top-view trajectory generated ({num_frames} frames)")
    
    # Step 4: Render frames with scaling
    print("\n[4/5] Rendering frames...")
    renderer = SceneRenderer(output_size=output_size)
    
    char_image, char_mask = char_handler.get_character_data()
    env_image = env_handler.get_environment_data()
    
    angles = np.linspace(0, 2 * np.pi, num_frames, endpoint=False)
    frames = renderer.render_frames(
        char_image, 
        char_mask, 
        env_image, 
        angles,
        character_scale=1.2  # Scale up character
    )
    print(f"  ✓ Rendered {len(frames)} frames with 1.2x character scale")
    
    # Step 5: Generate video
    print("\n[5/5] Generating video...")
    video_gen = VideoGenerator(fps=fps)
    video_gen.add_frames(frames)
    video_gen.generate_video(output_file)
    print(f"  ✓ Video saved: {output_file}")
    print(f"  ✓ Duration: {video_gen.get_video_duration():.2f} seconds")
    
    print("\n" + "=" * 60)
    print("✓ Advanced example complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
