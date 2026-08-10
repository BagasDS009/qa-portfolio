import allure
import pytest

from tests.test_data import BOOK_PAYLOAD


@allure.epic("FakeREST API")
@allure.feature("Books")
class TestBooks:
    """Test suite for /Books endpoints."""

    @allure.title("GET all books returns 200 and a list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_books(self, api_context):
        with allure.step("Send GET request to /Books"):
            response = api_context.get("/api/v1/Books")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("GET single book by ID returns 200 with required fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_book_by_id(self, api_context):
        with allure.step("Send GET request to /Books/1"):
            response = api_context.get("/api/v1/Books/1")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response contains required fields"):
            data = response.json()
            assert "id" in data
            assert "title" in data
            assert "pageCount" in data
            assert "publishDate" in data
            assert data["id"] == 1

    @allure.title("POST create a new book returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_create_book(self, api_context):
        with allure.step("Send POST request to /Books"):
            response = api_context.post("/api/v1/Books", data=BOOK_PAYLOAD)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body matches payload"):
            data = response.json()
            assert data["id"] == BOOK_PAYLOAD["id"]
            assert data["title"] == BOOK_PAYLOAD["title"]
            assert data["pageCount"] == BOOK_PAYLOAD["pageCount"]
            assert data["description"] == BOOK_PAYLOAD["description"]

    @allure.title("PUT update an existing book returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_update_book(self, api_context):
        updated_payload = {
            **BOOK_PAYLOAD,
            "title": "Updated Book Title",
            "pageCount": 500,
        }

        with allure.step("Send PUT request to /Books/999"):
            response = api_context.put("/api/v1/Books/999", data=updated_payload)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body reflects updates"):
            data = response.json()
            assert data["title"] == "Updated Book Title"
            assert data["pageCount"] == 500

    @allure.title("DELETE a book returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_delete_book(self, api_context):
        with allure.step("Send DELETE request to /Books/999"):
            response = api_context.delete("/api/v1/Books/999")

        with allure.step("Verify status code is 200"):
            assert response.status == 200
