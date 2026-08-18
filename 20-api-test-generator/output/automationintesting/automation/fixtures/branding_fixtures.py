"""Branding fixtures — provides BrandingClient."""

import pytest

from api.branding_client import BrandingClient


@pytest.fixture()
def branding_client(admin_token: str) -> BrandingClient:
    """Authenticated BrandingClient."""
    client = BrandingClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def branding_client_unauth() -> BrandingClient:
    """Unauthenticated BrandingClient."""
    client = BrandingClient()
    yield client
    client.close()
