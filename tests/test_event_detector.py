import pytest
from unittest.mock import patch, MagicMock
from src.event_detector import EventDetector

@pytest.fixture
def mock_image_analysis_service():
    """Provides a mock ImageAnalysisService."""
    return MagicMock()

@pytest.fixture
def detector(mock_image_analysis_service):
    """Provides an EventDetector instance for tests."""
    return EventDetector(mock_image_analysis_service)

def test_detect_events_bowl_empty(detector, mock_image_analysis_service):
    """
    Unit test for the 'dog food from the bowl is all gone' event.
    """
    # Arrange
    mock_image_analysis_service.analyze_image.return_value = "empty"
    frame = "dummy_frame"

    # Act
    with patch.object(detector, '_save_frame_to_disk', return_value='dummy_path') as mock_save:
        event = detector.detect_events(frame)

    # Assert
    assert event == "dog food from the bowl is all gone"

def test_detect_events_bowl_refilled(detector, mock_image_analysis_service):
    """
    Unit test for the 'dog food is refilled' event.
    """
    # Arrange
    mock_image_analysis_service.analyze_image.return_value = "full"
    frame = "dummy_frame"

    # Act
    with patch.object(detector, '_save_frame_to_disk', return_value='dummy_path') as mock_save:
        event = detector.detect_events(frame)

    # Assert
    assert event == "dog food is refilled"

def test_detect_events_partially_eaten(detector, mock_image_analysis_service):
    """
    Unit test for the 'dog has eaten the food but did not finish all' event.
    """
    # Arrange
    mock_image_analysis_service.analyze_image.return_value = "partially eaten"
    frame = "dummy_frame"

    # Act
    with patch.object(detector, '_save_frame_to_disk', return_value='dummy_path') as mock_save:
        event = detector.detect_events(frame)

    # Assert
    assert event == "dog has eaten the food but did not finish all"
