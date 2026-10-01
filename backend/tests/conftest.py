import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.database import Base, get_db
from app.main import app

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")


class Config:
    """Create config class with environment variables."""

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://"
        + POSTGRES_USER
        + ":"
        + POSTGRES_PASSWORD
        + "@localhost/"
        + POSTGRES_DB
    )
    TESTING = True


@pytest.fixture(scope="session")
def db_engine_testing():
    """Create the test database if needed, and prepare its schema.

    Runs once per pytest session, against a database named after
    POSTGRES_DB with a "_test" suffix — never against the dev database
    itself.

    Yields:
        The SQLAlchemy engine bound to the test database.

    """
    admin_url = Config.SQLALCHEMY_DATABASE_URI
    admin_engine = create_engine(admin_url)
    admin_connection = admin_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    )
    database_test = POSTGRES_DB + "_test"
    exists = admin_connection.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :name"),
        {"name": database_test},
    ).scalar()
    if not exists:
        admin_connection.execute(text(f"CREATE DATABASE {database_test}"))
    admin_connection.close()
    admin_engine.dispose()
    config_test = admin_url + "_test"
    engine = create_engine(config_test)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(db_engine_testing):
    """Give each test its own connection wrapped in a savepoint.

    Uses join_transaction_mode="create_savepoint" so that a db.commit() made
    by the code under test only releases a SAVEPOINT, not the outer
    transaction — the final transaction.rollback() still undoes everything,
    including data that code under test explicitly committed.

    Yields:
        A SQLAlchemy session bound to this per-test transaction.

    """
    connection = db_engine_testing.connect()
    transaction = connection.begin()
    testing_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
        join_transaction_mode="create_savepoint",
    )
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client_fastapi(test_db):
    """Build a TestClient whose get_db dependency is overridden to use test_db.

    Without this override, TestClient(app) would use the app's real
    get_db, hitting the dev database instead of the isolated test one.

    Yields:
        A starlette TestClient wired to the test database, unauthenticated.

    """

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def authenticated_test_client(client_fastapi):
    """Register and log in a test user.

    The login response sets the access_token cookie, which the TestClient
    stores and sends back automatically on every following request.

    Returns:
        The client_fastapi client, holding the access_token cookie so it can
        call routes protected by get_current_user.

    """
    client_fastapi.post(
        "/auth/authentification",
        json={"login": "test", "password": "test", "email": "test@test.com"},
    )

    client_fastapi.post(
        "/auth/login", data={"username": "test", "password": "test"}
    )

    return client_fastapi


@pytest.fixture(scope="function")
def second_authenticated_test_client(test_db):
    """Create a client authenticated as a second, distinct user.

    NOTE: this exists specifically to test ownership scoping (e.g. a
    restaurant/plat created by user A must not be visible/editable by user
    B) — not just the happy path. Worth reusing wherever a route filters by
    `current_user.id`.

    Returns:
        A TestClient authenticated as "test2", independent from the client
        returned by authenticated_test_client.

    """

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    client.post(
        "/auth/authentification",
        json={"login": "test2", "password": "test2", "email": "test2@test.com"},
    )
    client.post("/auth/login", data={"username": "test2", "password": "test2"})

    try:
        yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def create_restaurant(authenticated_test_client):
    """Create a restaurant owned by the authenticated test user.

    Returns:
        The raw Response from POST /restaurants/restaurant.

    """
    return authenticated_test_client.post(
        "/restaurants/restaurant",
        json={"nom": "test_restaurant", "categorie": "test_categorie"},
    )


@pytest.fixture(scope="function")
def create_plat(authenticated_test_client, create_restaurant):
    """Create a dish for the authenticated test user's restaurant.

    Depends on create_restaurant so the dish always has a valid, owned
    id_restaurant to attach to.

    Returns:
        The raw Response from POST /plats/plat.

    """
    id_restaurant = create_restaurant.json()["id"]
    return authenticated_test_client.post(
        "/plats/plat",
        json={
            "nom": "test_plat",
            "categorie": "test_categorie",
            "id_restaurant": id_restaurant,
        },
    )


@pytest.fixture(scope="function")
def create_ingredient(authenticated_test_client):
    """Create an ingredient via the API.

    Returns:
        The raw Response from POST /ingredients/ingredient.

    """
    return authenticated_test_client.post(
        "/ingredients/ingredient", json={"nom": "test_ingredient"}
    )


@pytest.fixture(scope="function")
def create_allergene(authenticated_test_client):
    """Create an allergene via the API.

    Returns:
        The raw Response from POST /allergenes/allergene.

    """
    return authenticated_test_client.post(
        "/allergenes/allergene", json={"nom": "test_allergene"}
    )
