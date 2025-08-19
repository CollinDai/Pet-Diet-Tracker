import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from src.services.monitoring_service import MonitoringService, MonitoringResult
from tests.mocks.mock_camera import MockCamera
from tests.mocks.mock_notification_service import MockNotificationService

@pytest.fixture
def mock_services():
    """Create mock services for testing."""
    notification_service = MockNotificationService()
    event_history_service = MagicMock()
    return notification_service, event_history_service

@pytest.fixture 
def monitoring_service(mock_services):
    """Create monitoring service with mocked dependencies."""
    notification_service, event_history_service = mock_services
    return MonitoringService(notification_service, event_history_service, debounce_time=3600)

def test_monitoring_cycle_complete_flow(monitoring_service, mock_services):
    """
    Test the complete monitoring flow: capture -> analyze -> detect -> handle event.
    """
    notification_service, event_history_service = mock_services
    
    # Create mock frame (simulating a captured image)
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_camera = MockCamera([mock_frame])
    
    # Mock the event detection to return a specific event
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food is refilled"):
        result = monitoring_service.run_monitoring_cycle(mock_camera)
    
    # Assertions
    assert isinstance(result, MonitoringResult)
    assert result.frame_captured is True
    assert result.event_detected == "dog food is refilled"
    assert result.error is None
    assert len(notification_service.notifications) == 1
    event_history_service.log_event.assert_called_once_with("dog food is refilled")

def test_monitoring_cycle_no_event_detected(monitoring_service, mock_services):
    """
    Test monitoring cycle when no event is detected.
    """
    notification_service, event_history_service = mock_services
    
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_camera = MockCamera([mock_frame])
    
    # Mock no event detection
    with patch.object(monitoring_service.detector, 'detect_events', return_value=None):
        result = monitoring_service.run_monitoring_cycle(mock_camera)
    
    # Assertions
    assert result.frame_captured is True
    assert result.event_detected is None
    assert result.error is None
    assert len(notification_service.notifications) == 0
    event_history_service.log_event.assert_not_called()

def test_monitoring_cycle_camera_failure(monitoring_service):
    """
    Test monitoring cycle when camera fails to capture frame.
    """
    # Create a camera that returns failure
    mock_camera = MagicMock()
    mock_camera.read.return_value = (False, None)
    
    result = monitoring_service.run_monitoring_cycle(mock_camera)
    
    # Assertions
    assert result.frame_captured is False
    assert result.event_detected is None
    assert result.error == "Failed to capture frame from camera"

def test_monitoring_cycle_event_detection_error(monitoring_service, mock_services):
    """
    Test monitoring cycle when event detection fails.
    """
    notification_service, event_history_service = mock_services
    
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_camera = MockCamera([mock_frame])
    
    # Mock event detection to raise an exception
    with patch.object(monitoring_service.detector, 'detect_events', side_effect=Exception("Detection failed")):
        result = monitoring_service.run_monitoring_cycle(mock_camera)
    
    # Assertions
    assert result.frame_captured is True
    assert result.event_detected is None
    assert result.error == "Failed to detect events: Detection failed"
    assert len(notification_service.notifications) == 0

def test_monitoring_cycle_notification_error(monitoring_service, mock_services):
    """
    Test monitoring cycle when notification sending fails.
    """
    notification_service, event_history_service = mock_services
    
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_camera = MockCamera([mock_frame])
    
    # Mock notification service to raise an exception
    notification_service.send_notification = MagicMock(side_effect=Exception("Notification failed"))
    
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food is refilled"):
        result = monitoring_service.run_monitoring_cycle(mock_camera)
    
    # Assertions
    assert result.frame_captured is True
    assert result.event_detected == "dog food is refilled"
    assert result.error == "Failed to handle event: Notification failed"

@patch('time.time')
def test_event_debouncing(mock_time, monitoring_service, mock_services):
    """
    Test that events are properly debounced to prevent spam.
    """
    notification_service, event_history_service = mock_services
    
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # First event at time 1000
    mock_time.return_value = 1000
    mock_camera1 = MockCamera([mock_frame])
    
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food is refilled"):
        result1 = monitoring_service.run_monitoring_cycle(mock_camera1)
    
    assert len(notification_service.notifications) == 1
    assert event_history_service.log_event.call_count == 1
    
    # Same event 30 minutes later (should be debounced)
    mock_time.return_value = 1000 + 1800  # 30 minutes later
    mock_camera2 = MockCamera([mock_frame])
    
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food is refilled"):
        result2 = monitoring_service.run_monitoring_cycle(mock_camera2)
    
    assert len(notification_service.notifications) == 1  # Still only 1
    assert event_history_service.log_event.call_count == 1  # Still only called once
    
    # Same event 2 hours later (should trigger again)
    mock_time.return_value = 1000 + 7200  # 2 hours later
    mock_camera3 = MockCamera([mock_frame])
    
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food is refilled"):
        result3 = monitoring_service.run_monitoring_cycle(mock_camera3)
    
    assert len(notification_service.notifications) == 2  # Now 2
    assert event_history_service.log_event.call_count == 2  # Called twice
    
    # Different event immediately (should trigger)
    mock_camera4 = MockCamera([mock_frame])
    
    with patch.object(monitoring_service.detector, 'detect_events', return_value="dog food from the bowl is all gone"):
        result4 = monitoring_service.run_monitoring_cycle(mock_camera4)
    
    assert len(notification_service.notifications) == 3  # Now 3
    assert event_history_service.log_event.call_count == 3  # Called three times

def test_multiple_monitoring_cycles(monitoring_service, mock_services):
    """
    Test multiple monitoring cycles with different events.
    """
    notification_service, event_history_service = mock_services
    
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Define a sequence of events
    events = [
        "dog food is refilled",
        None,  # No event
        "dog has eaten the food but did not finish all",
        "dog food from the bowl is all gone"
    ]
    
    results = []
    for event in events:
        mock_camera = MockCamera([mock_frame])
        with patch.object(monitoring_service.detector, 'detect_events', return_value=event):
            result = monitoring_service.run_monitoring_cycle(mock_camera)
            results.append(result)
    
    # Verify all cycles completed successfully
    assert all(result.frame_captured for result in results)
    assert all(result.error is None for result in results)
    
    # Verify events were detected correctly
    assert results[0].event_detected == "dog food is refilled"
    assert results[1].event_detected is None
    assert results[2].event_detected == "dog has eaten the food but did not finish all"
    assert results[3].event_detected == "dog food from the bowl is all gone"
    
    # Verify notifications were sent for detected events only
    assert len(notification_service.notifications) == 3
    assert event_history_service.log_event.call_count == 3