"""Tests for the POST /activities/{activity_name}/signup endpoint."""


def test_signup_new_participant(client):
    """Test successfully signing up a new participant.
    
    AAA Pattern:
    - Arrange: Prepare a new email address and activity name
    - Act: Send POST request to signup endpoint
    - Assert: Verify success response and confirmation message
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "チェスクラブ"  # Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]


def test_signup_nonexistent_activity(client):
    """Test signup to a non-existent activity returns 404.
    
    AAA Pattern:
    - Arrange: Prepare email and non-existent activity name
    - Act: Send POST request with invalid activity
    - Assert: Verify 404 error response
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "NonexistentActivity"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    error = response.json()
    assert "detail" in error


def test_signup_duplicate_participant(client):
    """Test that duplicate signup returns 409 conflict.
    
    AAA Pattern:
    - Arrange: Get existing participant and activity
    - Act: Send POST request for duplicate signup
    - Assert: Verify 409 conflict response
    """
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "チェスクラブ"  # Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 409
    error = response.json()
    assert "detail" in error


def test_signup_email_normalization_lowercase(client):
    """Test that uppercase email is normalized to lowercase.
    
    AAA Pattern:
    - Arrange: Prepare uppercase email and verify it normalizes
    - Act: Send POST request with uppercase email
    - Assert: Verify signup succeeds and email is normalized in response
    """
    # Arrange
    email_upper = "TestStudent@MERGINGTON.EDU"
    email_normalized = "teststudent@mergington.edu"
    activity = "プログラミングクラス"  # Programming Class
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email_upper}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert email_normalized in result["message"]


def test_signup_email_normalization_whitespace(client):
    """Test that email with whitespace is normalized.
    
    AAA Pattern:
    - Arrange: Prepare email with leading/trailing whitespace
    - Act: Send POST request with whitespace email
    - Assert: Verify signup succeeds and email is stripped
    """
    # Arrange
    email_with_space = "  whitespace@mergington.edu  "
    email_normalized = "whitespace@mergington.edu"
    activity = "体育クラス"  # Gym Class
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email_with_space}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert email_normalized in result["message"]


def test_signup_verifies_participant_added(client):
    """Test that participant is actually added to activity.
    
    AAA Pattern:
    - Arrange: Sign up new participant
    - Act: Retrieve activities to verify
    - Assert: Verify participant is in the activity's participant list
    """
    # Arrange
    email = "verify@mergington.edu"
    activity = "サッカーチーム"  # Soccer Team
    
    # Act
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    get_response = client.get("/activities")
    activities = get_response.json()
    
    # Assert
    assert signup_response.status_code == 200
    assert email in activities[activity]["participants"]
