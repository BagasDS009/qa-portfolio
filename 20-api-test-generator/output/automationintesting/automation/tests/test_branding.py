"""Test suite for /branding endpoints — Read and Update (singleton resource)."""

import allure
import pytest

from api.branding_client import BrandingClient
from config.settings import Config


@allure.epic("Restful Booker Platform")
@allure.feature("Branding")
class TestBrandingRead:
    """GET /branding — read operations (public)."""

    @allure.title("TC-BRAND-001: GET /branding returns branding object")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_get_branding(self, branding_client_unauth: BrandingClient):
        with allure.step("GET /branding"):
            response = branding_client_unauth.get_branding()

        with allure.step("Verify 200 + branding object"):
            assert response.status_code == 200
            data = response.json()
            assert "name" in data
            assert "map" in data
            assert "contact" in data

    @allure.title("TC-BRAND-002: GET /branding response time < 2s")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_branding_response_time(self, branding_client_unauth: BrandingClient):
        import time

        with allure.step("GET /branding and measure time"):
            start = time.time()
            response = branding_client_unauth.get_branding()
            elapsed_ms = (time.time() - start) * 1000

        with allure.step(f"Verify response time {elapsed_ms:.0f}ms < {Config.RESPONSE_TIME_BUDGET_MS}ms"):
            assert response.status_code == 200
            assert elapsed_ms < Config.RESPONSE_TIME_BUDGET_MS


@allure.epic("Restful Booker Platform")
@allure.feature("Branding")
class TestBrandingUpdate:
    """PUT /branding — update operations (requires auth).

    NOTE: logoUrl must be a full URL (https://...) for the API validator to accept it.
    The GET endpoint returns a relative path, but PUT requires absolute URL.
    """

    @allure.title("TC-BRAND-003: Update branding with valid data returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.wave1
    def test_update_branding_valid(self, branding_client: BrandingClient):
        # First get current branding to restore after
        get_resp = branding_client.get_branding()
        assert get_resp.status_code == 200
        original = get_resp.json()

        updated_data = original.copy()
        updated_data["description"] = "Updated description for test validation"
        # API BUG: logoUrl stored as relative but validated as URL — fix for update
        if updated_data.get("logoUrl", "").startswith("/"):
            updated_data["logoUrl"] = f"https://automationintesting.online{updated_data['logoUrl']}"

        with allure.step("PUT /branding"):
            response = branding_client.update_branding(updated_data)

        with allure.step("Verify 200 + success"):
            assert response.status_code == 200

        # Restore original (best-effort, don't fail test if restore has network issue)
        try:
            restore = original.copy()
            if restore.get("logoUrl", "").startswith("/"):
                restore["logoUrl"] = f"https://automationintesting.online{restore['logoUrl']}"
            branding_client.update_branding(restore)
        except Exception:
            pass  # Shared API — restore is best-effort

    @allure.title("TC-BRAND-004: Update branding without auth returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_update_branding_no_auth(self, branding_client_unauth: BrandingClient):
        with allure.step("PUT /branding without auth"):
            response = branding_client_unauth.update_branding({"name": "Hacked"})

        with allure.step("Verify 401"):
            assert response.status_code == 401


@allure.epic("Restful Booker Platform")
@allure.feature("Branding")
class TestBrandingContract:
    """Schema/contract validation for branding responses."""

    @allure.title("TC-BRAND-005: Branding object has required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_branding_schema(self, branding_client_unauth: BrandingClient):
        with allure.step("GET /branding"):
            response = branding_client_unauth.get_branding()

        with allure.step("Verify branding schema"):
            assert response.status_code == 200
            data = response.json()
            required_fields = {"name", "logoUrl", "description", "map", "contact"}
            assert required_fields.issubset(set(data.keys()))
            assert isinstance(data["name"], str)
            assert isinstance(data["map"], dict)
            assert "latitude" in data["map"]
            assert "longitude" in data["map"]
            assert isinstance(data["contact"], dict)
            assert "name" in data["contact"]
            assert "email" in data["contact"]
            assert "phone" in data["contact"]

    @allure.title("TC-BRAND-006: Branding map coordinates are valid numbers")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_branding_map_coordinates(self, branding_client_unauth: BrandingClient):
        with allure.step("GET /branding"):
            response = branding_client_unauth.get_branding()

        with allure.step("Verify map coordinates are floats"):
            assert response.status_code == 200
            map_data = response.json()["map"]
            assert isinstance(map_data["latitude"], (int, float))
            assert isinstance(map_data["longitude"], (int, float))
            # Sanity check — coordinates should be in valid range
            assert -90 <= map_data["latitude"] <= 90
            assert -180 <= map_data["longitude"] <= 180
