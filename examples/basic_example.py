#!/usr/bin/env python3
"""
Basic example of using the panoramic video generator programmatically.

This example creates a simple panoramic video with a character on a gradient background.
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


def create_sample_character():
    """Create a simple sample character (a circle) for demonstration."""
    size = 200
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    mask = np.zeros((size, size), dtype=np.uint8)
    
    # Draw a circle
    center = size // 2
    y, x = np.ogrid[:size, :size]
    circle_mask = (x - center) ** 2 + (y - center) ** 2 <= (size // 3) ** 2
    
    # Red circle
    img[circle_mask] = [255, 0, 0]
    mask[circle_mask] = 255
    
    return img, mask


def main():
    """Main example function."""
    print("=" * 60)
    print("Basic Panoramic Video Generation Example")
    print("=" * 60)
    
    # Configuration
    num_frames = 60
    fps = 30
    output_size = (1280, 720)
    output_file = "examples/output_basic.mp4"
    
    # Ensure output directory exists
    os.makedirs("examples", exist_ok=True)
    
    # Step 1: Create sample character
    print("\n[1/5] Creating sample character...")
    char_handler = CharacterHandler()
    char_img, char_mask = create_sample_character()
    char_handler.load_character_from_array(char_img, char_mask)
    print("  ✓ Sample character created")
    
    # Step 2: Create environment
    print("\n[2/5] Creating gradient environment...")
    env_handler = EnvironmentHandler()
    env_handler.create_gradient_environment(
        top_color=(135, 206, 235),  # Sky blue
        bottom_color=(34, 139, 34),  # Forest green
        size=output_size
    )
    print("  ✓ Gradient environment created")
    
    # Step 3: Generate camera trajectory
    print("\n[3/5] Generating circular camera trajectory...")
    camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=num_frames)
    camera.generate_circular_trajectory(center=(0, 0, 0))
    print(f"  ✓ Trajectory generated ({num_frames} frames)")
    
    # Step 4: Render frames
    print("\n[4/5] Rendering frames...")
    renderer = SceneRenderer(output_size=output_size)
    
    char_image, char_mask = char_handler.get_character_data()
    env_image = env_handler.get_environment_data()
    
    angles = np.linspace(0, 2 * np.pi, num_frames, endpoint=False)
    frames = renderer.render_frames(char_image, char_mask, env_image, angles)
    print(f"  ✓ Rendered {len(frames)} frames")
    
    # Step 5: Generate video
    print("\n[5/5] Generating video...")
    video_gen = VideoGenerator(fps=fps)
    video_gen.add_frames(frames)
    video_gen.generate_video(output_file)
    print(f"  ✓ Video saved: {output_file}")
    print(f"  ✓ Duration: {video_gen.get_video_duration():.2f} seconds")
    
    print("\n" + "=" * 60)
    print("✓ Example complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
