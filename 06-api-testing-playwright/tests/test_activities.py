import allure
import pytest

from tests.test_data import ACTIVITY_PAYLOAD


@allure.epic("FakeREST API")
@allure.feature("Activities")
class TestActivities:
    """Test suite for /Activities endpoints."""

    @allure.title("GET all activities returns 200 and a list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_activities(self, api_context):
        with allure.step("Send GET request to /Activities"):
            response = api_context.get("/api/v1/Activities")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("GET single activity by ID returns 200 with correct fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_activity_by_id(self, api_context):
        with allure.step("Send GET request to /Activities/1"):
            response = api_context.get("/api/v1/Activities/1")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response contains correct fields"):
            data = response.json()
            assert "id" in data
            assert "title" in data
            assert "dueDate" in data
            assert "completed" in data
            assert data["id"] == 1

    @allure.title("GET non-existent activity returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_get_activity_not_found(self, api_context):
        with allure.step("Send GET request to /Activities/99999"):
            response = api_context.get("/api/v1/Activities/99999")

        with allure.step("Verify status code is 404"):
            assert response.status == 404

    @allure.title("POST create a new activity returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_create_activity(self, api_context):
        with allure.step("Send POST request to /Activities"):
            response = api_context.post("/api/v1/Activities", data=ACTIVITY_PAYLOAD)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body matches payload"):
            data = response.json()
            assert data["id"] == ACTIVITY_PAYLOAD["id"]
            assert data["title"] == ACTIVITY_PAYLOAD["title"]
            assert data["completed"] == ACTIVITY_PAYLOAD["completed"]

    @allure.title("PUT update an existing activity returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_update_activity(self, api_context):
        updated_payload = {
            **ACTIVITY_PAYLOAD,
            "title": "Updated Activity",
            "completed": True,
        }

        with allure.step("Send PUT request to /Activities/999"):
            response = api_context.put("/api/v1/Activities/999", data=updated_payload)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body reflects updates"):
            data = response.json()
            assert data["title"] == "Updated Activity"
            assert data["completed"] is True

    @allure.title("DELETE an activity returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_delete_activity(self, api_context):
        with allure.step("Send DELETE request to /Activities/999"):
            response = api_context.delete("/api/v1/Activities/999")

        with allure.step("Verify status code is 200"):
            assert response.status == 200
