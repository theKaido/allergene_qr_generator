def test_get_all_user(authenticated_test_client):
    """Test that GET /auth/authentification lists registered users."""
    response = authenticated_test_client.get("/auth/authentification")
    assert response.status_code == 200
    logins = [user["login"] for user in response.json()]
    assert "test" in logins


def test_create_new_user(client_fastapi):
    """Test POST /auth/authentification, success and duplicate login."""
    response = client_fastapi.post(
        "/auth/authentification",
        json={"login": "new_user", "password": "azerty", "email": "new_user@test.com"},
    )
    assert response.status_code == 200
    assert response.json()["login"] == "new_user"

    # NOTE: the password comes back hashed here, not in clear text — worth
    # checking that create_new_user never leaks the plaintext password.
    assert response.json()["password"] != "azerty"

    response = client_fastapi.post(
        "/auth/authentification",
        json={"login": "new_user", "password": "azerty", "email": "new_user@test.com"},
    )
    assert response.status_code == 409


def test_login(client_fastapi):
    """Test POST /auth/login, success and wrong credentials."""
    client_fastapi.post(
        "/auth/authentification",
        json={
            "login": "login_user",
            "password": "azerty",
            "email": "login_user@test.com",
        },
    )

    response = client_fastapi.post(
        "/auth/login", data={"username": "login_user", "password": "azerty"}
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies

    response = client_fastapi.post(
        "/auth/login", data={"username": "login_user", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert "access_token" not in response.cookies

    response = client_fastapi.post(
        "/auth/login", data={"username": "unknown_user", "password": "azerty"}
    )
    assert response.status_code == 401


def test_update_password(authenticated_test_client):
    """Test PUT /auth/authentification/password, success and wrong current password."""
    response = authenticated_test_client.put(
        "/auth/authentification/password",
        json={"current_password": "wrong", "new_password": "new_test_password"},
    )
    assert response.status_code == 401

    response = authenticated_test_client.put(
        "/auth/authentification/password",
        json={"current_password": "test", "new_password": "new_test_password"},
    )
    assert response.status_code == 200

    # Confirm the new password actually works and the old one doesn't anymore.
    response = authenticated_test_client.post(
        "/auth/login", data={"username": "test", "password": "test"}
    )
    assert response.status_code == 401

    response = authenticated_test_client.post(
        "/auth/login", data={"username": "test", "password": "new_test_password"}
    )
    assert response.status_code == 200
