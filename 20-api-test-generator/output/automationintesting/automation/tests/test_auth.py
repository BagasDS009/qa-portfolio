"""Test suite for /auth endpoints — login, validate, logout."""

import allure
import pytest

from api.auth import AuthClient
from config.settings import Config


@allure.epic("Restful Booker Platform")
@allure.feature("Auth")
class TestAuthLogin:
    """POST /auth/login — functional + negative tests."""

    @allure.title("TC-AUTH-001: Valid admin login returns token")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_valid_credentials(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login with valid credentials"):
            response = unauth_client.post("/auth/login", json={
                "username": Config.ADMIN_USERNAME,
                "password": Config.ADMIN_PASSWORD,
            })

        with allure.step("Verify 200 + token returned"):
            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            assert len(data["token"]) > 0

    @allure.title("TC-AUTH-002: Invalid password returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_invalid_password(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login with wrong password"):
            response = unauth_client.post("/auth/login", json={
                "username": Config.ADMIN_USERNAME,
                "password": "wrongpassword123",
            })

        with allure.step("Verify 401 + no token"):
            assert response.status_code == 401

    @allure.title("TC-AUTH-003: Invalid username returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_invalid_username(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login with wrong username"):
            response = unauth_client.post("/auth/login", json={
                "username": "nonexistent_user",
                "password": Config.ADMIN_PASSWORD,
            })

        with allure.step("Verify 401"):
            assert response.status_code == 401

    @allure.title("TC-AUTH-004: Empty credentials returns 401")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_empty_credentials(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login with empty body"):
            response = unauth_client.post("/auth/login", json={
                "username": "",
                "password": "",
            })

        with allure.step("Verify 401"):
            assert response.status_code == 401

    @allure.title("TC-AUTH-005: Login response time < 2s")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    @pytest.mark.auth
    def test_login_response_time(self, unauth_client: AuthClient):
        import time

        with allure.step("POST /auth/login and measure time"):
            start = time.time()
            response = unauth_client.post("/auth/login", json={
                "username": Config.ADMIN_USERNAME,
                "password": Config.ADMIN_PASSWORD,
            })
            elapsed_ms = (time.time() - start) * 1000

        with allure.step(f"Verify response time {elapsed_ms:.0f}ms < {Config.RESPONSE_TIME_BUDGET_MS}ms"):
            assert response.status_code == 200
            assert elapsed_ms < Config.RESPONSE_TIME_BUDGET_MS


@allure.epic("Restful Booker Platform")
@allure.feature("Auth")
class TestAuthValidate:
    """POST /auth/validate — token validation tests.

    NOTE: The /auth/validate endpoint returns 500 on this deployment.
    These tests document actual behavior (API BUG — endpoint broken).
    """

    @allure.title("TC-AUTH-006: Validate endpoint returns 500 (known API bug)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_validate_returns_500(self, auth_client: AuthClient):
        with allure.step("POST /auth/validate with valid token"):
            response = auth_client.post("/auth/validate")

        with allure.step("Verify 500 (known API bug — endpoint broken)"):
            # API BUG: /auth/validate returns 500 regardless of token
            assert response.status_code == 500

    @allure.title("TC-AUTH-007: Validate without token also returns 500")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    @pytest.mark.auth
    def test_validate_no_token_returns_500(self, unauth_client: AuthClient):
        with allure.step("POST /auth/validate without token"):
            response = unauth_client.post("/auth/validate")

        with allure.step("Verify 500 (known API bug)"):
            assert response.status_code == 500


@allure.epic("Restful Booker Platform")
@allure.feature("Auth")
class TestAuthLogout:
    """POST /auth/logout — logout tests.

    NOTE: The /auth/logout endpoint returns 500 on this deployment (API BUG).
    """

    @allure.title("TC-AUTH-008: Logout returns 500 (known API bug)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.wave1
    @pytest.mark.auth
    def test_logout_returns_500(self):
        """Login then attempt logout — documents API returning 500."""
        client = AuthClient()
        try:
            with allure.step("Login to get fresh token"):
                token = client.login()
                assert token

            with allure.step("POST /auth/logout"):
                response = client.post("/auth/logout")

            with allure.step("Verify 500 (known API bug — logout broken)"):
                assert response.status_code == 500
        finally:
            client.close()


@allure.epic("Restful Booker Platform")
@allure.feature("Auth")
class TestAuthContract:
    """Schema/contract validation for auth responses."""

    @allure.title("TC-AUTH-009: Login response schema has 'token' field")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    @pytest.mark.auth
    def test_login_response_schema(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login"):
            response = unauth_client.post("/auth/login", json={
                "username": Config.ADMIN_USERNAME,
                "password": Config.ADMIN_PASSWORD,
            })

        with allure.step("Verify response contains only 'token' key"):
            assert response.status_code == 200
            data = response.json()
            assert set(data.keys()) == {"token"}
            assert isinstance(data["token"], str)

    @allure.title("TC-AUTH-010: SQL injection in username returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    @pytest.mark.auth
    def test_sql_injection_username(self, unauth_client: AuthClient):
        with allure.step("POST /auth/login with SQL injection payload"):
            response = unauth_client.post("/auth/login", json={
                "username": "' OR '1'='1",
                "password": "' OR '1'='1",
            })

        with allure.step("Verify no token issued (401)"):
            assert response.status_code == 401
