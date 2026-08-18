"""Auth fixtures — provides authenticated and unauthenticated clients."""

import pytest

from api.auth import AuthClient
from config.settings import Config


@pytest.fixture(scope="session")
def admin_token() -> str:
    """Login once per session and return admin token."""
    client = AuthClient()
    token = client.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
    assert token, "Admin login failed — check credentials in .env"
    client.close()
    return token


@pytest.fixture()
def auth_client(admin_token: str) -> AuthClient:
    """Authenticated AuthClient (fresh per test, shared token)."""
    client = AuthClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def unauth_client() -> AuthClient:
    """Unauthenticated AuthClient — no token set."""
    client = AuthClient()
    yield client
    client.close()
