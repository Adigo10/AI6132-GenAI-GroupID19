"""Environment Handler Module

This module handles environment/surrounding input processing.
"""

import numpy as np
from PIL import Image
from typing import Union, Optional, Tuple
import cv2


class EnvironmentHandler:
    """
    Handles environment/surrounding input processing for panoramic video generation.
    
    The environment forms the background around the central character.
    """
    
    def __init__(self):
        """Initialize the environment handler."""
        self.environment_image = None
        self.environment_type = None  # 'image', 'color', 'generated'
        self.environment_size = None
        
    def load_environment(self, image_path: str) -> None:
        """
        Load an environment image.
        
        Args:
            image_path: Path to the environment/background image file
        """
        self.environment_image = Image.open(image_path).convert('RGB')
        self.environment_size = self.environment_image.size
        self.environment_type = 'image'
    
    def load_environment_from_array(self, image_array: np.ndarray) -> None:
        """
        Load an environment from a numpy array.
        
        Args:
            image_array: Environment image as numpy array (H, W, 3)
        """
        self.environment_image = Image.fromarray(image_array, 'RGB')
        self.environment_size = self.environment_image.size
        self.environment_type = 'image'
    
    def create_solid_environment(self, color: Tuple[int, int, int], 
                                 size: Tuple[int, int] = (1920, 1080)) -> None:
        """
        Create a solid color environment.
        
        Args:
            color: RGB color tuple (r, g, b)
            size: Size of the environment (width, height)
        """
        env_array = np.full((size[1], size[0], 3), color, dtype=np.uint8)
        self.environment_image = Image.fromarray(env_array, 'RGB')
        self.environment_size = size
        self.environment_type = 'color'
    
    def create_gradient_environment(self, top_color: Tuple[int, int, int],
                                     bottom_color: Tuple[int, int, int],
                                     size: Tuple[int, int] = (1920, 1080)) -> None:
        """
        Create a gradient environment.
        
        Args:
            top_color: RGB color at the top (r, g, b)
            bottom_color: RGB color at the bottom (r, g, b)
            size: Size of the environment (width, height)
        """
        # Create gradient
        gradient = np.linspace(0, 1, size[1])[:, np.newaxis]
        top = np.array(top_color).reshape(1, 3)
        bottom = np.array(bottom_color).reshape(1, 3)
        
        env_array = (gradient * bottom + (1 - gradient) * top).astype(np.uint8)
        env_array = np.repeat(env_array[:, np.newaxis, :], size[0], axis=1)
        
        self.environment_image = Image.fromarray(env_array, 'RGB')
        self.environment_size = size
        self.environment_type = 'generated'
    
    def preprocess_environment(self, target_size: Optional[Tuple[int, int]] = None) -> None:
        """
        Preprocess the environment for rendering.
        
        Args:
            target_size: Optional target size (width, height) to resize environment to
        """
        if self.environment_image is None:
            raise ValueError("No environment loaded. Create or load an environment first.")
        
        if target_size:
            self.environment_image = self.environment_image.resize(
                target_size, Image.Resampling.LANCZOS
            )
            self.environment_size = target_size
    
    def get_environment_data(self) -> np.ndarray:
        """
        Get the processed environment image.
        
        Returns:
            Environment image as numpy array (H, W, 3)
        """
        if self.environment_image is None:
            raise ValueError("No environment loaded.")
        
        return np.array(self.environment_image)
    
    def get_environment_size(self) -> Tuple[int, int]:
        """
        Get the current environment size.
        
        Returns:
            Tuple of (width, height)
        """
        return self.environment_size
