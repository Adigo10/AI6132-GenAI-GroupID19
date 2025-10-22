"""
Panoramic Video Generator
==========================

A Gen AI project for generating 360-degree top-view panoramic videos
with a character centered in a surrounding environment.

This package provides tools for:
- Character input processing
- Environment/surrounding processing
- Circular camera trajectory generation
- 3D scene rendering
- Video generation pipeline
"""

__version__ = "0.1.0"
__author__ = "AI6132 Group 19"

from .core.character_handler import CharacterHandler
from .core.environment_handler import EnvironmentHandler
from .core.camera_trajectory import CameraTrajectory
from .core.scene_renderer import SceneRenderer
from .core.video_generator import VideoGenerator

__all__ = [
    'CharacterHandler',
    'EnvironmentHandler',
    'CameraTrajectory',
    'SceneRenderer',
    'VideoGenerator',
]
