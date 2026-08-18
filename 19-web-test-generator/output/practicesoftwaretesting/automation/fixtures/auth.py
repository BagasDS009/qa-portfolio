"""Authentication fixtures for logged-in test scenarios."""

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from test_data.users import VALID_CUSTOMER, VALID_ADMIN


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Provide a page that is already logged in as customer."""
    login_page = LoginPage(page)
    login_page.login(
        email=VALID_CUSTOMER["email"],
        password=VALID_CUSTOMER["password"],
    )
    page.wait_for_load_state("networkidle")
    return page


@pytest.fixture
def admin_page(page: Page) -> Page:
    """Provide a page logged in as admin."""
    login_page = LoginPage(page)
    login_page.login(
        email=VALID_ADMIN["email"],
        password=VALID_ADMIN["password"],
    )
    page.wait_for_load_state("networkidle")
    return page
