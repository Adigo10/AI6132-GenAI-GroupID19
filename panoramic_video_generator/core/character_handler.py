"""Character Handler Module

This module handles character input processing and preparation for rendering.
"""

import numpy as np
from PIL import Image
from typing import Union, Optional, Tuple
import cv2


class CharacterHandler:
    """
    Handles character input processing for panoramic video generation.
    
    The character will be positioned at the center of the scene in the final video.
    """
    
    def __init__(self):
        """Initialize the character handler."""
        self.character_image = None
        self.character_mask = None
        self.character_size = None
        
    def load_character(self, image_path: str, mask_path: Optional[str] = None) -> None:
        """
        Load a character image and optional mask.
        
        Args:
            image_path: Path to the character image file
            mask_path: Optional path to character mask/alpha channel
        """
        # Load the character image
        self.character_image = Image.open(image_path).convert('RGBA')
        self.character_size = self.character_image.size
        
        # Load or create mask
        if mask_path:
            mask_img = Image.open(mask_path).convert('L')
            self.character_mask = np.array(mask_img)
        else:
            # Use alpha channel if available, otherwise create from image
            if self.character_image.mode == 'RGBA':
                self.character_mask = np.array(self.character_image)[:, :, 3]
            else:
                # Create simple mask from non-white pixels
                img_array = np.array(self.character_image.convert('RGB'))
                self.character_mask = np.all(img_array < 250, axis=2).astype(np.uint8) * 255
    
    def load_character_from_array(self, image_array: np.ndarray, 
                                   mask_array: Optional[np.ndarray] = None) -> None:
        """
        Load a character from numpy arrays.
        
        Args:
            image_array: Character image as numpy array (H, W, C)
            mask_array: Optional mask as numpy array (H, W)
        """
        if image_array.shape[2] == 4:
            self.character_image = Image.fromarray(image_array, 'RGBA')
            self.character_mask = image_array[:, :, 3]
        else:
            self.character_image = Image.fromarray(image_array, 'RGB')
            if mask_array is not None:
                self.character_mask = mask_array
            else:
                # Create simple mask
                self.character_mask = np.all(image_array < 250, axis=2).astype(np.uint8) * 255
        
        self.character_size = self.character_image.size
    
    def preprocess_character(self, target_size: Optional[Tuple[int, int]] = None) -> None:
        """
        Preprocess the character for rendering.
        
        Args:
            target_size: Optional target size (width, height) to resize character to
        """
        if self.character_image is None:
            raise ValueError("No character loaded. Call load_character first.")
        
        if target_size:
            self.character_image = self.character_image.resize(target_size, Image.Resampling.LANCZOS)
            self.character_mask = cv2.resize(self.character_mask, target_size, 
                                            interpolation=cv2.INTER_LINEAR)
            self.character_size = target_size
    
    def get_character_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get the processed character image and mask.
        
        Returns:
            Tuple of (character_image, character_mask) as numpy arrays
        """
        if self.character_image is None:
            raise ValueError("No character loaded.")
        
        char_array = np.array(self.character_image)
        return char_array, self.character_mask
    
    def get_character_size(self) -> Tuple[int, int]:
        """
        Get the current character size.
        
        Returns:
            Tuple of (width, height)
        """
        return self.character_size
