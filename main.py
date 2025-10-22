#!/usr/bin/env python3
"""
Main application entry point for panoramic video generation.

This script provides a command-line interface for generating 360-degree
top-view panoramic videos with a character centered in the scene.
"""

import argparse
import sys
import numpy as np
from pathlib import Path

from panoramic_video_generator.core import (
    CharacterHandler,
    EnvironmentHandler,
    CameraTrajectory,
    SceneRenderer,
    VideoGenerator,
)
from panoramic_video_generator.utils import Config, ensure_dir


def main():
    """Main entry point for the panoramic video generator."""
    parser = argparse.ArgumentParser(
        description="Generate 360-degree top-view panoramic videos"
    )
    
    # Input arguments
    parser.add_argument(
        '--character',
        type=str,
        required=True,
        help='Path to character image file'
    )
    parser.add_argument(
        '--character-mask',
        type=str,
        default=None,
        help='Optional path to character mask/alpha channel'
    )
    parser.add_argument(
        '--environment',
        type=str,
        default=None,
        help='Path to environment/background image file'
    )
    parser.add_argument(
        '--env-type',
        type=str,
        choices=['image', 'color', 'gradient'],
        default='gradient',
        help='Environment type (default: gradient)'
    )
    parser.add_argument(
        '--env-color',
        type=int,
        nargs=3,
        default=[135, 206, 235],
        help='RGB color for solid environment (default: sky blue)'
    )
    
    # Output arguments
    parser.add_argument(
        '--output',
        type=str,
        default='output.mp4',
        help='Output video file path (default: output.mp4)'
    )
    parser.add_argument(
        '--output-frames',
        type=str,
        default=None,
        help='Optional directory to save individual frames'
    )
    
    # Video parameters
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frames per second (default: 30)'
    )
    parser.add_argument(
        '--num-frames',
        type=int,
        default=120,
        help='Total number of frames for 360-degree rotation (default: 120)'
    )
    parser.add_argument(
        '--resolution',
        type=int,
        nargs=2,
        default=[1920, 1080],
        help='Output resolution (width height, default: 1920 1080)'
    )
    
    # Camera parameters
    parser.add_argument(
        '--camera-radius',
        type=float,
        default=5.0,
        help='Camera distance from character (default: 5.0)'
    )
    parser.add_argument(
        '--camera-height',
        type=float,
        default=10.0,
        help='Camera height above scene (default: 10.0)'
    )
    parser.add_argument(
        '--top-view',
        action='store_true',
        help='Use pure top-down view instead of circular trajectory'
    )
    
    # Character parameters
    parser.add_argument(
        '--character-scale',
        type=float,
        default=1.0,
        help='Character scale factor (default: 1.0)'
    )
    
    # Configuration file
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to YAML configuration file'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = Config.from_yaml(args.config)
    else:
        config = Config()
    
    # Override config with command-line arguments
    config.set('video.fps', args.fps)
    config.set('video.num_frames', args.num_frames)
    config.set('video.output_size', args.resolution)
    config.set('camera.radius', args.camera_radius)
    config.set('camera.height', args.camera_height)
    config.set('character.scale', args.character_scale)
    
    print("=" * 60)
    print("360-Degree Panoramic Video Generator")
    print("=" * 60)
    
    # Load character
    print("\n[1/5] Loading character...")
    char_handler = CharacterHandler()
    try:
        char_handler.load_character(args.character, args.character_mask)
        print(f"  ✓ Character loaded: {args.character}")
        print(f"  ✓ Character size: {char_handler.get_character_size()}")
    except Exception as e:
        print(f"  ✗ Error loading character: {e}")
        sys.exit(1)
    
    # Load/create environment
    print("\n[2/5] Setting up environment...")
    env_handler = EnvironmentHandler()
    try:
        if args.environment:
            env_handler.load_environment(args.environment)
            print(f"  ✓ Environment loaded: {args.environment}")
        elif args.env_type == 'gradient':
            env_handler.create_gradient_environment(
                top_color=tuple(config.get('environment.gradient_top')),
                bottom_color=tuple(config.get('environment.gradient_bottom')),
                size=tuple(args.resolution)
            )
            print(f"  ✓ Gradient environment created")
        else:
            env_handler.create_solid_environment(
                color=tuple(args.env_color),
                size=tuple(args.resolution)
            )
            print(f"  ✓ Solid color environment created")
    except Exception as e:
        print(f"  ✗ Error setting up environment: {e}")
        sys.exit(1)
    
    # Generate camera trajectory
    print("\n[3/5] Generating camera trajectory...")
    camera = CameraTrajectory(
        radius=args.camera_radius,
        height=args.camera_height,
        num_frames=args.num_frames
    )
    
    if args.top_view:
        camera.generate_top_view_trajectory()
        print(f"  ✓ Top-view trajectory generated ({args.num_frames} frames)")
    else:
        camera.generate_circular_trajectory()
        print(f"  ✓ Circular trajectory generated ({args.num_frames} frames)")
    
    # Render frames
    print("\n[4/5] Rendering frames...")
    renderer = SceneRenderer(output_size=tuple(args.resolution))
    
    char_image, char_mask = char_handler.get_character_data()
    env_image = env_handler.get_environment_data()
    
    # Generate angles for camera rotation effect
    angles = np.linspace(0, 2 * np.pi, args.num_frames, endpoint=False)
    
    try:
        frames = renderer.render_frames(
            char_image,
            char_mask,
            env_image,
            angles,
            character_scale=args.character_scale
        )
        print(f"  ✓ Rendered {len(frames)} frames")
    except Exception as e:
        print(f"  ✗ Error rendering frames: {e}")
        sys.exit(1)
    
    # Generate video
    print("\n[5/5] Generating video...")
    video_gen = VideoGenerator(fps=args.fps)
    video_gen.add_frames(frames)
    
    try:
        # Ensure output directory exists
        output_path = Path(args.output)
        ensure_dir(str(output_path.parent) if output_path.parent != Path('.') else '.')
        
        # Generate video
        video_gen.generate_video(args.output)
        print(f"  ✓ Video saved: {args.output}")
        print(f"  ✓ Duration: {video_gen.get_video_duration():.2f} seconds")
        
        # Save individual frames if requested
        if args.output_frames:
            ensure_dir(args.output_frames)
            video_gen.save_frames_as_images(args.output_frames)
            print(f"  ✓ Frames saved to: {args.output_frames}")
            
    except Exception as e:
        print(f"  ✗ Error generating video: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
