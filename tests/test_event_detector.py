import pytest
import numpy as np
from unittest.mock import patch
from src.event_detector import EventDetector

@pytest.fixture
def detector():
    """Provides an EventDetector instance for tests."""
    return EventDetector()

def generate_dummy_frame():
    """Generates a simple black frame for testing."""
    return np.zeros((480, 640, 3), np.uint8)

@patch('cv2.findContours')
def test_detect_events_bowl_empty(mock_find_contours, detector):
    """
    Unit test for the 'dog food from the bowl is all gone' event.
    """
    # Arrange: Mock findContours to return 0 contours
    mock_find_contours.return_value = ([], None)
    frame = generate_dummy_frame()

    # Act
    event = detector.detect_events(frame)

    # Assert
    assert event == "dog food from the bowl is all gone"

@patch('cv2.findContours')
def test_detect_events_bowl_refilled(mock_find_contours, detector):
    """
    Unit test for the 'dog food is refilled' event.
    """
    # Arrange: Mock findContours to return a high number of contours (e.g., 30)
    # The actual contour data doesn't matter, just the length.
    mock_find_contours.return_value = ([1] * 30, None)
    frame = generate_dummy_frame()

    # Act
    event = detector.detect_events(frame)

    # Assert
    assert event == "dog food is refilled"

@patch('cv2.findContours')
def test_detect_events_partially_eaten(mock_find_contours, detector):
    """
    Unit test for the 'dog has eaten the food but did not finish all' event.
    """
    # Arrange: Mock findContours to return a medium number of contours (e.g., 15)
    mock_find_contours.return_value = ([1] * 15, None)
    frame = generate_dummy_frame()

    # Act
    event = detector.detect_events(frame)

    # Assert
    assert event == "dog has eaten the food but did not finish all"
