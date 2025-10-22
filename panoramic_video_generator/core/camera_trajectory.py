"""Camera Trajectory Module

This module generates circular camera trajectories for top-view 360-degree panoramic videos.
"""

import numpy as np
from typing import Tuple, Optional


class CameraTrajectory:
    """
    Generates circular camera trajectories for panoramic video generation.
    
    Creates a circular motion path around a central character for top-view rendering.
    """
    
    def __init__(self, radius: float = 5.0, height: float = 10.0, 
                 num_frames: int = 120):
        """
        Initialize camera trajectory generator.
        
        Args:
            radius: Radius of the circular path around the character
            height: Height of the camera above the scene (for top-view)
            num_frames: Number of frames in the 360-degree rotation
        """
        self.radius = radius
        self.height = height
        self.num_frames = num_frames
        self.camera_positions = None
        self.camera_targets = None
        self.camera_ups = None
        
    def generate_circular_trajectory(self, center: Tuple[float, float, float] = (0, 0, 0),
                                     start_angle: float = 0.0) -> None:
        """
        Generate a circular camera trajectory around a center point.
        
        Args:
            center: 3D position of the center (character position) (x, y, z)
            start_angle: Starting angle in radians
        """
        angles = np.linspace(start_angle, start_angle + 2 * np.pi, 
                            self.num_frames, endpoint=False)
        
        # Generate camera positions in a circle
        x_positions = center[0] + self.radius * np.cos(angles)
        y_positions = center[1] + self.radius * np.sin(angles)
        z_positions = np.full_like(angles, center[2] + self.height)
        
        self.camera_positions = np.stack([x_positions, y_positions, z_positions], axis=1)
        
        # All cameras look at the center
        self.camera_targets = np.tile(center, (self.num_frames, 1))
        
        # Up vector points in positive Z direction for top-view
        self.camera_ups = np.tile([0, 0, 1], (self.num_frames, 1))
    
    def generate_top_view_trajectory(self, center: Tuple[float, float, float] = (0, 0, 0),
                                     tilt_angle: float = 0.0) -> None:
        """
        Generate a top-view trajectory with optional tilt.
        
        Args:
            center: 3D position of the center (character position)
            tilt_angle: Angle to tilt the camera from pure top-down (radians)
        """
        if tilt_angle == 0:
            # Pure top-down view, camera doesn't move in XY
            self.camera_positions = np.tile(
                [center[0], center[1], center[2] + self.height], 
                (self.num_frames, 1)
            )
            
            # Rotate the target point around the center
            angles = np.linspace(0, 2 * np.pi, self.num_frames, endpoint=False)
            target_x = center[0] + 0.1 * np.cos(angles)  # Small offset for orientation
            target_y = center[1] + 0.1 * np.sin(angles)
            target_z = np.full_like(angles, center[2])
            
            self.camera_targets = np.stack([target_x, target_y, target_z], axis=1)
            
            # Up vector rotates to maintain orientation
            up_x = -np.sin(angles)
            up_y = np.cos(angles)
            up_z = np.zeros_like(angles)
            
            self.camera_ups = np.stack([up_x, up_y, up_z], axis=1)
        else:
            # Tilted circular trajectory
            self.generate_circular_trajectory(center)
            
    def get_camera_parameters(self, frame_idx: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get camera parameters for a specific frame.
        
        Args:
            frame_idx: Frame index
            
        Returns:
            Tuple of (position, target, up) vectors
        """
        if self.camera_positions is None:
            raise ValueError("Trajectory not generated. Call generate_*_trajectory first.")
        
        return (self.camera_positions[frame_idx],
                self.camera_targets[frame_idx],
                self.camera_ups[frame_idx])
    
    def get_all_camera_parameters(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get all camera parameters.
        
        Returns:
            Tuple of (positions, targets, ups) arrays (N x 3)
        """
        if self.camera_positions is None:
            raise ValueError("Trajectory not generated.")
        
        return self.camera_positions, self.camera_targets, self.camera_ups
    
    def set_num_frames(self, num_frames: int) -> None:
        """
        Update the number of frames (requires regenerating trajectory).
        
        Args:
            num_frames: New number of frames
        """
        self.num_frames = num_frames
        self.camera_positions = None
        self.camera_targets = None
        self.camera_ups = None
