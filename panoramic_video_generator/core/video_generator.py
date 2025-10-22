"""Video Generator Module

This module handles the video generation pipeline from rendered frames.
"""

import numpy as np
from typing import List, Optional, Tuple
import cv2
from tqdm import tqdm
import os


class VideoGenerator:
    """
    Generates video from rendered frames with 360-degree panoramic motion.
    """
    
    def __init__(self, fps: int = 30):
        """
        Initialize the video generator.
        
        Args:
            fps: Frames per second for the output video
        """
        self.fps = fps
        self.frames = []
        
    def add_frame(self, frame: np.ndarray) -> None:
        """
        Add a frame to the video.
        
        Args:
            frame: Frame as numpy array (H, W, 3)
        """
        self.frames.append(frame)
    
    def add_frames(self, frames: List[np.ndarray]) -> None:
        """
        Add multiple frames to the video.
        
        Args:
            frames: List of frames as numpy arrays
        """
        self.frames.extend(frames)
    
    def generate_video(self, output_path: str, codec: str = 'mp4v') -> None:
        """
        Generate video file from frames.
        
        Args:
            output_path: Path to save the output video
            codec: Video codec (default: 'mp4v')
        """
        if not self.frames:
            raise ValueError("No frames to generate video. Add frames first.")
        
        # Get frame dimensions
        height, width = self.frames[0].shape[:2]
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))
        
        # Write frames
        print(f"Generating video with {len(self.frames)} frames at {self.fps} fps...")
        for frame in tqdm(self.frames, desc="Writing frames"):
            # Convert RGB to BGR for OpenCV
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(bgr_frame)
        
        out.release()
        print(f"Video saved to: {output_path}")
    
    def generate_video_with_moviepy(self, output_path: str, 
                                    audio_path: Optional[str] = None) -> None:
        """
        Generate video using MoviePy (better quality and format support).
        
        Args:
            output_path: Path to save the output video
            audio_path: Optional path to audio file to add to video
        """
        try:
            from moviepy.editor import ImageSequenceClip, AudioFileClip
        except ImportError:
            raise ImportError("MoviePy not installed. Install with: pip install moviepy")
        
        if not self.frames:
            raise ValueError("No frames to generate video. Add frames first.")
        
        print(f"Generating video with {len(self.frames)} frames at {self.fps} fps...")
        
        # Create video clip from frames
        clip = ImageSequenceClip([frame for frame in self.frames], fps=self.fps)
        
        # Add audio if provided
        if audio_path and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            clip = clip.set_audio(audio)
        
        # Write video file
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac',
                            fps=self.fps, verbose=False, logger=None)
        
        print(f"Video saved to: {output_path}")
    
    def save_frames_as_images(self, output_dir: str, prefix: str = "frame") -> None:
        """
        Save individual frames as image files.
        
        Args:
            output_dir: Directory to save frames
            prefix: Prefix for frame filenames
        """
        if not self.frames:
            raise ValueError("No frames to save.")
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Saving {len(self.frames)} frames to {output_dir}...")
        for idx, frame in enumerate(tqdm(self.frames, desc="Saving frames")):
            filename = os.path.join(output_dir, f"{prefix}_{idx:05d}.png")
            # Convert RGB to BGR for OpenCV
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, bgr_frame)
        
        print(f"Frames saved to: {output_dir}")
    
    def clear_frames(self) -> None:
        """Clear stored frames to free memory."""
        self.frames = []
    
    def get_num_frames(self) -> int:
        """
        Get the number of frames currently stored.
        
        Returns:
            Number of frames
        """
        return len(self.frames)
    
    def get_video_duration(self) -> float:
        """
        Get the duration of the video in seconds.
        
        Returns:
            Video duration in seconds
        """
        return len(self.frames) / self.fps
