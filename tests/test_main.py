import pytest
from unittest.mock import patch, MagicMock
from src.main import main_loop
from src.services.monitoring_service import MonitoringService, MonitoringResult
from tests.mocks.mock_camera import MockCamera
from tests.mocks.mock_notification_service import MockNotificationService

def test_main_loop_event_detection():
    """
    Tests the main loop with a mock camera and monitoring service.
    """
    # Arrange
    frames = ["frame1", "frame2", "frame3"]
    mock_camera = MockCamera(frames)
    mock_monitoring_service = MagicMock()
    
    # Mock monitoring service to call the camera.read() method and track frame index
    def mock_run_cycle(camera):
        camera.read()  # This advances frame_index
        return MonitoringResult("dog food is refilled", True, 1000)
    
    mock_monitoring_service.run_monitoring_cycle.side_effect = mock_run_cycle

    # Act
    main_loop(mock_camera, mock_monitoring_service)

    # Assert
    assert mock_monitoring_service.run_monitoring_cycle.call_count == 3


def test_main_loop_no_events():
    """
    Tests that main loop handles cases when no events are detected.
    """
    # Arrange
    frames = ["frame1", "frame2", "frame3"]
    mock_camera = MockCamera(frames)
    mock_monitoring_service = MagicMock()
    
    # Mock monitoring service to call the camera.read() method and track frame index
    def mock_run_cycle(camera):
        camera.read()  # This advances frame_index
        return MonitoringResult(None, True, 1000)
    
    mock_monitoring_service.run_monitoring_cycle.side_effect = mock_run_cycle

    # Act
    main_loop(mock_camera, mock_monitoring_service)

    # Assert
    assert mock_monitoring_service.run_monitoring_cycle.call_count == 3

def test_main_loop_camera_failure():
    """
    Tests that main loop handles camera failures gracefully.
    """
    # Arrange
    mock_camera = MockCamera([])  # Empty frames will cause camera failure
    mock_monitoring_service = MagicMock()
    
    # Mock monitoring service to return camera failure
    mock_monitoring_service.run_monitoring_cycle.return_value = MonitoringResult(
        None, False, 1000, "Failed to capture frame from camera"
    )

    # Act
    main_loop(mock_camera, mock_monitoring_service)

    # Assert
    assert mock_monitoring_service.run_monitoring_cycle.call_count == 1

def test_main_loop_monitoring_error():
    """
    Tests that main loop continues even when monitoring service has errors.
    """
    # Arrange
    frames = ["frame1", "frame2"]
    mock_camera = MockCamera(frames)
    mock_monitoring_service = MagicMock()
    
    # Mock monitoring service to call the camera.read() method and track frame index
    call_count = [0]
    def mock_run_cycle(camera):
        camera.read()  # This advances frame_index
        call_count[0] += 1
        if call_count[0] == 1:
            return MonitoringResult(None, True, 1000, "Some monitoring error")
        else:
            return MonitoringResult("dog food is refilled", True, 1001)
    
    mock_monitoring_service.run_monitoring_cycle.side_effect = mock_run_cycle

    # Act
    main_loop(mock_camera, mock_monitoring_service)

    # Assert
    assert mock_monitoring_service.run_monitoring_cycle.call_count == 2
