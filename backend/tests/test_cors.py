from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_cors_preflight_allowed_origin() -> None:
    """Preflight from the frontend origin is accepted with credentials."""
    response = client.options(
        "/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_preflight_disallowed_origin() -> None:
    """Preflight from an unknown origin is rejected."""
    response = client.options(
        "/auth/login",
        headers={
            "Origin": "http://evil.com",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
