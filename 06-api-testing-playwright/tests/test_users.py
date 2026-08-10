import allure
import pytest

from tests.test_data import USER_PAYLOAD


@allure.epic("FakeREST API")
@allure.feature("Users")
class TestUsers:
    """Test suite for /Users endpoints."""

    @allure.title("GET all users returns 200 and a list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_users(self, api_context):
        with allure.step("Send GET request to /Users"):
            response = api_context.get("/api/v1/Users")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("GET single user by ID returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_user_by_id(self, api_context):
        with allure.step("Send GET request to /Users/1"):
            response = api_context.get("/api/v1/Users/1")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response contains correct fields"):
            data = response.json()
            assert "id" in data
            assert "userName" in data
            assert "password" in data
            assert data["id"] == 1

    @allure.title("POST create a new user returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_create_user(self, api_context):
        with allure.step("Send POST request to /Users"):
            response = api_context.post("/api/v1/Users", data=USER_PAYLOAD)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body matches payload"):
            data = response.json()
            assert data["id"] == USER_PAYLOAD["id"]
            assert data["userName"] == USER_PAYLOAD["userName"]
            assert data["password"] == USER_PAYLOAD["password"]

    @allure.title("PUT update an existing user returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_update_user(self, api_context):
        updated_payload = {
            **USER_PAYLOAD,
            "userName": "updateduser",
            "password": "Updated@456",
        }

        with allure.step("Send PUT request to /Users/999"):
            response = api_context.put("/api/v1/Users/999", data=updated_payload)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body reflects updates"):
            data = response.json()
            assert data["userName"] == "updateduser"
            assert data["password"] == "Updated@456"

    @allure.title("DELETE a user returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_delete_user(self, api_context):
        with allure.step("Send DELETE request to /Users/999"):
            response = api_context.delete("/api/v1/Users/999")

        with allure.step("Verify status code is 200"):
            assert response.status == 200
