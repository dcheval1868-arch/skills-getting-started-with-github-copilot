"""Tests for the GET /activities endpoint."""


def test_get_all_activities(client):
    """Test that all activities can be retrieved.
    
    AAA Pattern:
    - Arrange: Test client is ready
    - Act: Send GET request to /activities
    - Assert: Verify response status and data structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9  # There are 9 activities defined


def test_get_activities_contains_required_fields(client):
    """Test that each activity contains all required fields.
    
    AAA Pattern:
    - Arrange: Test client is ready
    - Act: Send GET request to /activities
    - Assert: Verify each activity has required fields
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_specific_activity(client):
    """Test that we can retrieve specific activity data.
    
    AAA Pattern:
    - Arrange: Test client is ready, know activity name
    - Act: Send GET request to /activities
    - Assert: Verify specific activity exists with correct structure
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert "チェスクラブ" in activities  # Chess Club in Japanese
    chess_club = activities["チェスクラブ"]
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) >= 0
