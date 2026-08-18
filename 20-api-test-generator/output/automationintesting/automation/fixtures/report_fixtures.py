"""Report fixtures — provides ReportClient."""

import pytest

from api.report_client import ReportClient


@pytest.fixture()
def report_client(admin_token: str) -> ReportClient:
    """Authenticated ReportClient."""
    client = ReportClient()
    client.set_token(admin_token)
    yield client
    client.close()


@pytest.fixture()
def report_client_unauth() -> ReportClient:
    """Unauthenticated ReportClient."""
    client = ReportClient()
    yield client
    client.close()
