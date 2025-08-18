import pytest
from unittest.mock import patch
from src.web_server import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('src.web_server.event_history_service')
def test_index_page_shows_events(mock_event_history_service, client):
    """
    Tests that the main page correctly displays events from the history service.
    """
    # Arrange
    mock_events = [
        {"timestamp": "2025-08-16T12:00:00", "event": "dog food is refilled"},
        {"timestamp": "2025-08-16T12:30:00", "event": "dog has eaten the food but did not finish all"}
    ]
    mock_event_history_service.get_events.return_value = mock_events

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    response_data = response.get_data(as_text=True)
    assert "Event History" in response_data
    assert "dog food is refilled" in response_data
    assert "dog has eaten the food but did not finish all" in response_data

@patch('src.web_server.event_history_service')
def test_index_page_no_events(mock_event_history_service, client):
    """
    Tests that the main page handles the case where there are no events.
    """
    # Arrange
    mock_event_history_service.get_events.return_value = []

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    response_data = response.get_data(as_text=True)
    assert "Event History" in response_data
    # Check that the table body is empty or contains a message (depending on implementation)
    # For now, just checking that the headers are there is sufficient.
    assert "Timestamp" in response_data
    assert "Event" in response_data
