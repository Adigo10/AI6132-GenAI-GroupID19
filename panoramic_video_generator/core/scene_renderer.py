"""Scene Renderer Module

This module handles 3D scene rendering with character and environment composition.
"""

import numpy as np
from typing import Tuple, Optional, List
import cv2
from PIL import Image


class SceneRenderer:
    """
    Renders the 3D scene with character and environment for each camera position.
    
    Composites the character at the center with the surrounding environment.
    """
    
    def __init__(self, output_size: Tuple[int, int] = (1920, 1080)):
        """
        Initialize the scene renderer.
        
        Args:
            output_size: Output frame size (width, height)
        """
        self.output_size = output_size
        self.frames = []
        
    def render_frame(self, 
                    character_image: np.ndarray,
                    character_mask: np.ndarray,
                    environment_image: np.ndarray,
                    camera_angle: float = 0.0,
                    character_scale: float = 1.0) -> np.ndarray:
        """
        Render a single frame with character and environment.
        
        Args:
            character_image: Character image array (H, W, C)
            character_mask: Character mask array (H, W)
            environment_image: Environment image array (H, W, 3)
            camera_angle: Current camera angle (for rotation effects)
            character_scale: Scale factor for character size
            
        Returns:
            Rendered frame as numpy array (H, W, 3)
        """
        # Resize environment to output size
        env_frame = cv2.resize(environment_image, self.output_size, 
                              interpolation=cv2.INTER_LINEAR)
        
        # Prepare character with rotation based on camera angle
        char_h, char_w = character_image.shape[:2]
        
        # Apply scale
        if character_scale != 1.0:
            new_w = int(char_w * character_scale)
            new_h = int(char_h * character_scale)
            character_image = cv2.resize(character_image, (new_w, new_h),
                                        interpolation=cv2.INTER_LINEAR)
            character_mask = cv2.resize(character_mask, (new_w, new_h),
                                       interpolation=cv2.INTER_LINEAR)
            char_h, char_w = new_h, new_w
        
        # Rotate character based on camera angle (optional effect)
        if camera_angle != 0.0:
            rotation_matrix = cv2.getRotationMatrix2D((char_w/2, char_h/2), 
                                                      np.degrees(camera_angle), 1.0)
            character_image = cv2.warpAffine(character_image, rotation_matrix, 
                                            (char_w, char_h))
            character_mask = cv2.warpAffine(character_mask, rotation_matrix, 
                                           (char_w, char_h))
        
        # Calculate position to center character in frame
        center_x = self.output_size[0] // 2
        center_y = self.output_size[1] // 2
        
        x_start = max(0, center_x - char_w // 2)
        y_start = max(0, center_y - char_h // 2)
        x_end = min(self.output_size[0], x_start + char_w)
        y_end = min(self.output_size[1], y_start + char_h)
        
        # Adjust character dimensions if it exceeds frame bounds
        char_x_start = 0 if x_start == center_x - char_w // 2 else (center_x - char_w // 2 - x_start)
        char_y_start = 0 if y_start == center_y - char_h // 2 else (center_y - char_h // 2 - y_start)
        char_x_end = char_w if x_end == x_start + char_w else char_x_start + (x_end - x_start)
        char_y_end = char_h if y_end == y_start + char_h else char_y_start + (y_end - y_start)
        
        # Composite character onto environment using alpha blending
        roi = env_frame[y_start:y_end, x_start:x_end]
        char_crop = character_image[char_y_start:char_y_end, char_x_start:char_x_end]
        mask_crop = character_mask[char_y_start:char_y_end, char_x_start:char_x_end]
        
        # Ensure character is RGB
        if char_crop.shape[2] == 4:
            char_crop = char_crop[:, :, :3]
        
        # Normalize mask to 0-1 range
        mask_normalized = mask_crop.astype(float) / 255.0
        mask_3channel = np.stack([mask_normalized] * 3, axis=2)
        
        # Alpha blending
        blended = (char_crop * mask_3channel + roi * (1 - mask_3channel)).astype(np.uint8)
        env_frame[y_start:y_end, x_start:x_end] = blended
        
        return env_frame
    
    def render_frames(self,
                     character_image: np.ndarray,
                     character_mask: np.ndarray,
                     environment_image: np.ndarray,
                     camera_angles: np.ndarray,
                     character_scale: float = 1.0) -> List[np.ndarray]:
        """
        Render all frames for the video.
        
        Args:
            character_image: Character image array
            character_mask: Character mask array
            environment_image: Environment image array
            camera_angles: Array of camera angles for each frame
            character_scale: Scale factor for character
            
        Returns:
            List of rendered frames
        """
        self.frames = []
        
        for angle in camera_angles:
            frame = self.render_frame(character_image, character_mask, 
                                     environment_image, angle, character_scale)
            self.frames.append(frame)
        
        return self.frames
    
    def get_frames(self) -> List[np.ndarray]:
        """
        Get the rendered frames.
        
        Returns:
            List of rendered frames
        """
        return self.frames
    
    def clear_frames(self) -> None:
        """Clear stored frames to free memory."""
        self.frames = []
