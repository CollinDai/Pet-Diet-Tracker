import pytest
from unittest.mock import patch, MagicMock
from src.main import main_loop
from tests.mocks.mock_camera import MockCamera
from tests.mocks.mock_notification_service import MockNotificationService

@patch('src.main.EventDetector')
@patch('src.main.EventHistoryService')
def test_main_loop_event_detection(MockEventHistoryService, MockEventDetector):
    """
    Tests the main loop with a mock camera and mock notification service.
    """
    # Arrange
    mock_event_detector_instance = MockEventDetector.return_value
    mock_event_detector_instance.detect_events.side_effect = [
        "dog food is refilled",
        "dog has eaten the food but did not finish all",
        "dog food from the bowl is all gone"
    ]
    frames = ["frame1", "frame2", "frame3"]
    mock_camera = MockCamera(frames)
    mock_notification_service = MockNotificationService()
    mock_event_history_service = MockEventHistoryService()

    # Act
    main_loop(mock_camera, mock_notification_service, mock_event_history_service)

    # Assert
    assert len(mock_notification_service.notifications) == 3
    assert mock_event_history_service.log_event.call_count == 3
    mock_event_history_service.log_event.assert_any_call("dog food is refilled")
    mock_event_history_service.log_event.assert_any_call("dog has eaten the food but did not finish all")
    mock_event_history_service.log_event.assert_any_call("dog food from the bowl is all gone")


@patch('src.main.EventDetector')
@patch('src.main.EventHistoryService')
def test_main_loop_no_events(MockEventHistoryService, MockEventDetector):
    """
    Tests that no notifications are sent when no events are detected.
    """
    # Arrange
    mock_event_detector_instance = MockEventDetector.return_value
    mock_event_detector_instance.detect_events.return_value = None
    frames = ["frame1", "frame2", "frame3"]
    mock_camera = MockCamera(frames)
    mock_notification_service = MockNotificationService()
    mock_event_history_service = MockEventHistoryService()

    # Act
    main_loop(mock_camera, mock_notification_service, mock_event_history_service)

    # Assert
    assert len(mock_notification_service.notifications) == 0
    assert mock_event_history_service.log_event.call_count == 0

@patch('time.time')
@patch('src.main.EventDetector')
@patch('src.main.EventHistoryService')
def test_main_loop_same_event_suppression(MockEventHistoryService, MockEventDetector, mock_time):
    """
    Tests that repeated events are suppressed for a period of time.
    """
    # Arrange
    mock_time.return_value = 1000
    mock_event_detector_instance = MockEventDetector.return_value
    mock_event_detector_instance.detect_events.return_value = "dog food is refilled"
    mock_notification_service = MockNotificationService()
    mock_event_history_service = MockEventHistoryService()
    
    # 1. Initial event
    frames = ["frame1"]
    mock_camera = MockCamera(frames)
    last_event, last_event_time = main_loop(mock_camera, mock_notification_service, mock_event_history_service)
    assert len(mock_notification_service.notifications) == 1
    assert mock_event_history_service.log_event.call_count == 1
    assert last_event == "dog food is refilled"

    # 2. Time advances, but not enough to trigger a new notification for the same event
    mock_time.return_value = 1000 + 3500
    frames = ["frame1"]
    mock_camera = MockCamera(frames)
    last_event, last_event_time = main_loop(mock_camera, mock_notification_service, mock_event_history_service, last_event, last_event_time)
    assert len(mock_notification_service.notifications) == 1
    assert mock_event_history_service.log_event.call_count == 1 # Should not be called again

    # 3. Time advances enough to trigger a new notification for the same event
    mock_time.return_value = 1000 + 3601
    frames = ["frame1"]
    mock_camera = MockCamera(frames)
    last_event, last_event_time = main_loop(mock_camera, mock_notification_service, mock_event_history_service, last_event, last_event_time)
    assert len(mock_notification_service.notifications) == 2
    assert mock_event_history_service.log_event.call_count == 2 # Should be called again
    
    # 4. A different event occurs, so a notification should be sent immediately
    mock_event_detector_instance.detect_events.return_value = "dog food from the bowl is all gone"
    frames = ["frame1"]
    mock_camera = MockCamera(frames)
    last_event, last_event_time = main_loop(mock_camera, mock_notification_service, mock_event_history_service, last_event, last_event_time)
    assert len(mock_notification_service.notifications) == 3
    assert mock_event_history_service.log_event.call_count == 3
