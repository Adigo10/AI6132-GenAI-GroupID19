"""Utility functions for panoramic video generation."""

import numpy as np
from typing import Tuple
import os


def ensure_dir(directory: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory: Path to directory
    """
    os.makedirs(directory, exist_ok=True)


def validate_image_array(image: np.ndarray, expected_channels: int = 3) -> bool:
    """
    Validate that an image array has the correct shape.
    
    Args:
        image: Image array to validate
        expected_channels: Expected number of channels
        
    Returns:
        True if valid, False otherwise
    """
    if image is None:
        return False
    if len(image.shape) != 3:
        return False
    if image.shape[2] != expected_channels:
        return False
    return True


def normalize_angle(angle: float) -> float:
    """
    Normalize angle to [0, 2*pi) range.
    
    Args:
        angle: Angle in radians
        
    Returns:
        Normalized angle
    """
    return angle % (2 * np.pi)


def interpolate_frames(frames: list, target_count: int) -> list:
    """
    Interpolate frames to reach target count.
    
    Args:
        frames: List of frames
        target_count: Target number of frames
        
    Returns:
        Interpolated list of frames
    """
    if len(frames) == target_count:
        return frames
    
    indices = np.linspace(0, len(frames) - 1, target_count)
    interpolated = []
    
    for idx in indices:
        lower = int(np.floor(idx))
        upper = int(np.ceil(idx))
        
        if lower == upper:
            interpolated.append(frames[lower])
        else:
            # Linear interpolation between frames
            alpha = idx - lower
            frame_blend = (frames[lower] * (1 - alpha) + frames[upper] * alpha).astype(np.uint8)
            interpolated.append(frame_blend)
    
    return interpolated


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Filename or path
        
    Returns:
        File extension (lowercase, without dot)
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')


def format_time(seconds: float) -> str:
    """
    Format time in seconds to human-readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs:.1f}s"
    elif minutes > 0:
        return f"{minutes}m {secs:.1f}s"
    else:
        return f"{secs:.1f}s"
