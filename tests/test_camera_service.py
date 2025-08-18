import pytest
from unittest.mock import patch, MagicMock
from src.services.camera_service import CameraService

@patch('src.services.camera_service.Picamera2')
def test_camera_service_initialization(MockPicamera2):
    """
    Tests that the CameraService initializes Picamera2 correctly.
    """
    # Arrange
    mock_picamera2_instance = MockPicamera2.return_value
    
    # Act
    camera_service = CameraService()
    
    # Assert
    MockPicamera2.assert_called_once()
    mock_picamera2_instance.configure.assert_called_once()
    mock_picamera2_instance.start.assert_called_once()

@patch('src.services.camera_service.Picamera2')
def test_camera_service_read_frame(MockPicamera2):
    """
    Tests that the CameraService can read a frame.
    """
    # Arrange
    mock_picamera2_instance = MockPicamera2.return_value
    mock_frame = "test_frame"
    mock_picamera2_instance.capture_array.return_value = mock_frame
    mock_picamera2_instance.started = True
    
    camera_service = CameraService()
    
    # Act
    ret, frame = camera_service.read()
    
    # Assert
    assert ret is True
    assert frame == mock_frame
    mock_picamera2_instance.capture_array.assert_called_once()

@patch('src.services.camera_service.Picamera2')
def test_camera_service_release(MockPicamera2):
    """
    Tests that the CameraService releases the camera correctly.
    """
    # Arrange
    mock_picamera2_instance = MockPicamera2.return_value
    mock_picamera2_instance.started = True
    
    camera_service = CameraService()
    
    # Act
    camera_service.release()
    
    # Assert
    mock_picamera2_instance.stop.assert_called_once()

@patch('src.services.camera_service.Picamera2')
def test_camera_service_isOpened(MockPicamera2):
    """
    Tests the isOpened method.
    """
    # Arrange
    mock_picamera2_instance = MockPicamera2.return_value
    
    # Case 1: Camera is started
    mock_picamera2_instance.started = True
    camera_service = CameraService()
    assert camera_service.isOpened() is True
    
    # Case 2: Camera is not started
    mock_picamera2_instance.started = False
    camera_service = CameraService()
    assert camera_service.isOpened() is False
