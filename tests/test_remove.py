"""Tests for the DELETE /activities/{activity_name}/remove endpoint."""


def test_remove_existing_participant(client):
    """Test successfully removing an existing participant.
    
    AAA Pattern:
    - Arrange: Sign up a participant first
    - Act: Send DELETE request to remove endpoint
    - Assert: Verify success response and confirmation message
    """
    # Arrange
    email = "remove_test@mergington.edu"
    activity = "バスケットボールクラブ"  # Basketball Club
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act
    response = client.delete(
        f"/activities/{activity}/remove",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]


def test_remove_nonexistent_activity(client):
    """Test removing participant from non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare email and non-existent activity name
    - Act: Send DELETE request with invalid activity
    - Assert: Verify 404 error response
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "NonexistentActivity"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/remove",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    error = response.json()
    assert "detail" in error


def test_remove_nonexistent_participant(client):
    """Test removing non-existent participant returns 404.
    
    AAA Pattern:
    - Arrange: Use email that's not registered in activity
    - Act: Send DELETE request for non-existent participant
    - Assert: Verify 404 error response
    """
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "アートワークショップ"  # Art Workshop
    
    # Act
    response = client.delete(
        f"/activities/{activity}/remove",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    error = response.json()
    assert "detail" in error


def test_remove_verifies_participant_removed(client):
    """Test that participant is actually removed from activity.
    
    AAA Pattern:
    - Arrange: Sign up participant
    - Act: Remove participant and verify
    - Assert: Verify participant is no longer in activity
    """
    # Arrange
    email = "verify_remove@mergington.edu"
    activity = "スクールバンド"  # School Band
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Act
    client.delete(f"/activities/{activity}/remove", params={"email": email})
    get_response = client.get("/activities")
    activities = get_response.json()
    
    # Assert
    assert email not in activities[activity]["participants"]


def test_remove_email_normalization(client):
    """Test that email is normalized when removing participant.
    
    AAA Pattern:
    - Arrange: Sign up with lowercase, prepare uppercase for removal
    - Act: Remove using uppercase/whitespace email
    - Assert: Verify removal succeeds despite different casing
    """
    # Arrange
    email_lower = "normalize_remove@mergington.edu"
    email_upper = "NORMALIZE_REMOVE@MERGINGTON.EDU"
    activity = "ディベート協会"  # Debate Society
    client.post(f"/activities/{activity}/signup", params={"email": email_lower})
    
    # Act
    response = client.delete(
        f"/activities/{activity}/remove",
        params={"email": email_upper}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
