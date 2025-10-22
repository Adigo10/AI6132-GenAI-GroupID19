"""
Unit tests for the panoramic video generator.

Run tests with: python -m pytest tests/
"""

import pytest
import numpy as np
from PIL import Image
import os
import tempfile

from panoramic_video_generator.core import (
    CharacterHandler,
    EnvironmentHandler,
    CameraTrajectory,
    SceneRenderer,
    VideoGenerator,
)
from panoramic_video_generator.utils import Config


class TestCharacterHandler:
    """Test character handler functionality."""
    
    def test_character_handler_init(self):
        """Test character handler initialization."""
        handler = CharacterHandler()
        assert handler.character_image is None
        assert handler.character_mask is None
        assert handler.character_size is None
    
    def test_load_character_from_array(self):
        """Test loading character from numpy array."""
        handler = CharacterHandler()
        
        # Create test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        test_mask = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        
        handler.load_character_from_array(test_image, test_mask)
        
        assert handler.character_image is not None
        assert handler.character_mask is not None
        assert handler.character_size == (100, 100)
    
    def test_get_character_data(self):
        """Test getting character data."""
        handler = CharacterHandler()
        
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        handler.load_character_from_array(test_image)
        
        char_img, char_mask = handler.get_character_data()
        assert char_img.shape[0] == 100
        assert char_img.shape[1] == 100


class TestEnvironmentHandler:
    """Test environment handler functionality."""
    
    def test_environment_handler_init(self):
        """Test environment handler initialization."""
        handler = EnvironmentHandler()
        assert handler.environment_image is None
        assert handler.environment_type is None
    
    def test_create_solid_environment(self):
        """Test creating solid color environment."""
        handler = EnvironmentHandler()
        handler.create_solid_environment(color=(255, 0, 0), size=(640, 480))
        
        assert handler.environment_image is not None
        assert handler.environment_type == 'color'
        assert handler.environment_size == (640, 480)
        
        env_data = handler.get_environment_data()
        assert env_data.shape == (480, 640, 3)
        assert np.all(env_data == [255, 0, 0])
    
    def test_create_gradient_environment(self):
        """Test creating gradient environment."""
        handler = EnvironmentHandler()
        handler.create_gradient_environment(
            top_color=(255, 255, 255),
            bottom_color=(0, 0, 0),
            size=(640, 480)
        )
        
        assert handler.environment_image is not None
        assert handler.environment_type == 'generated'
        assert handler.environment_size == (640, 480)
        
        env_data = handler.get_environment_data()
        assert env_data.shape == (480, 640, 3)


class TestCameraTrajectory:
    """Test camera trajectory generation."""
    
    def test_camera_trajectory_init(self):
        """Test camera trajectory initialization."""
        camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=60)
        assert camera.radius == 5.0
        assert camera.height == 10.0
        assert camera.num_frames == 60
    
    def test_generate_circular_trajectory(self):
        """Test circular trajectory generation."""
        camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=60)
        camera.generate_circular_trajectory(center=(0, 0, 0))
        
        positions, targets, ups = camera.get_all_camera_parameters()
        
        assert positions.shape == (60, 3)
        assert targets.shape == (60, 3)
        assert ups.shape == (60, 3)
        
        # Check that all cameras look at center
        assert np.allclose(targets, [0, 0, 0])
    
    def test_generate_top_view_trajectory(self):
        """Test top-view trajectory generation."""
        camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=60)
        camera.generate_top_view_trajectory(center=(0, 0, 0))
        
        positions, targets, ups = camera.get_all_camera_parameters()
        
        assert positions.shape == (60, 3)
        assert targets.shape == (60, 3)
        assert ups.shape == (60, 3)
    
    def test_get_camera_parameters(self):
        """Test getting camera parameters for specific frame."""
        camera = CameraTrajectory(radius=5.0, height=10.0, num_frames=60)
        camera.generate_circular_trajectory()
        
        pos, target, up = camera.get_camera_parameters(0)
        
        assert pos.shape == (3,)
        assert target.shape == (3,)
        assert up.shape == (3,)


class TestSceneRenderer:
    """Test scene renderer functionality."""
    
    def test_scene_renderer_init(self):
        """Test scene renderer initialization."""
        renderer = SceneRenderer(output_size=(640, 480))
        assert renderer.output_size == (640, 480)
        assert len(renderer.frames) == 0
    
    def test_render_frame(self):
        """Test rendering a single frame."""
        renderer = SceneRenderer(output_size=(640, 480))
        
        # Create test data
        char_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        char_mask = np.ones((100, 100), dtype=np.uint8) * 255
        env_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        frame = renderer.render_frame(char_image, char_mask, env_image)
        
        assert frame.shape == (480, 640, 3)
        assert frame.dtype == np.uint8
    
    def test_render_frames(self):
        """Test rendering multiple frames."""
        renderer = SceneRenderer(output_size=(640, 480))
        
        char_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        char_mask = np.ones((100, 100), dtype=np.uint8) * 255
        env_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        angles = np.linspace(0, 2 * np.pi, 10, endpoint=False)
        
        frames = renderer.render_frames(char_image, char_mask, env_image, angles)
        
        assert len(frames) == 10
        assert frames[0].shape == (480, 640, 3)


class TestVideoGenerator:
    """Test video generator functionality."""
    
    def test_video_generator_init(self):
        """Test video generator initialization."""
        gen = VideoGenerator(fps=30)
        assert gen.fps == 30
        assert len(gen.frames) == 0
    
    def test_add_frame(self):
        """Test adding a single frame."""
        gen = VideoGenerator(fps=30)
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        gen.add_frame(frame)
        
        assert gen.get_num_frames() == 1
    
    def test_add_frames(self):
        """Test adding multiple frames."""
        gen = VideoGenerator(fps=30)
        frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(10)]
        gen.add_frames(frames)
        
        assert gen.get_num_frames() == 10
    
    def test_get_video_duration(self):
        """Test calculating video duration."""
        gen = VideoGenerator(fps=30)
        frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(60)]
        gen.add_frames(frames)
        
        assert gen.get_video_duration() == 2.0  # 60 frames at 30 fps = 2 seconds
    
    def test_generate_video(self):
        """Test video generation."""
        gen = VideoGenerator(fps=30)
        frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(30)]
        gen.add_frames(frames)
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate_video(output_path)
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestConfig:
    """Test configuration functionality."""
    
    def test_config_init(self):
        """Test configuration initialization."""
        config = Config()
        assert config.get('video.fps') == 30
        assert config.get('camera.radius') == 5.0
    
    def test_config_get_set(self):
        """Test getting and setting config values."""
        config = Config()
        
        config.set('video.fps', 60)
        assert config.get('video.fps') == 60
        
        config.set('custom.value', 123)
        assert config.get('custom.value') == 123
    
    def test_config_yaml(self):
        """Test saving and loading YAML config."""
        config = Config()
        config.set('video.fps', 60)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml_path = f.name
        
        try:
            config.save_yaml(yaml_path)
            assert os.path.exists(yaml_path)
            
            loaded_config = Config.from_yaml(yaml_path)
            assert loaded_config.get('video.fps') == 60
        finally:
            if os.path.exists(yaml_path):
                os.remove(yaml_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
