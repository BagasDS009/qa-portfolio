import allure
import pytest

from tests.test_data import AUTHOR_PAYLOAD


@allure.epic("FakeREST API")
@allure.feature("Authors")
class TestAuthors:
    """Test suite for /Authors endpoints."""

    @allure.title("GET all authors returns 200 and a list")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_authors(self, api_context):
        with allure.step("Send GET request to /Authors"):
            response = api_context.get("/api/v1/Authors")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("GET single author by ID returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_author_by_id(self, api_context):
        with allure.step("Send GET request to /Authors/1"):
            response = api_context.get("/api/v1/Authors/1")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response contains correct fields"):
            data = response.json()
            assert "id" in data
            assert "idBook" in data
            assert "firstName" in data
            assert "lastName" in data
            assert data["id"] == 1

    @allure.title("GET authors by book ID returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_get_authors_by_book_id(self, api_context):
        with allure.step("Send GET request to /Authors/authors/books/1"):
            response = api_context.get("/api/v1/Authors/authors/books/1")

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)

    @allure.title("POST create a new author returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_create_author(self, api_context):
        with allure.step("Send POST request to /Authors"):
            response = api_context.post("/api/v1/Authors", data=AUTHOR_PAYLOAD)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body matches payload"):
            data = response.json()
            assert data["id"] == AUTHOR_PAYLOAD["id"]
            assert data["firstName"] == AUTHOR_PAYLOAD["firstName"]
            assert data["lastName"] == AUTHOR_PAYLOAD["lastName"]
            assert data["idBook"] == AUTHOR_PAYLOAD["idBook"]

    @allure.title("PUT update an existing author returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    def test_update_author(self, api_context):
        updated_payload = {
            **AUTHOR_PAYLOAD,
            "firstName": "Updated",
            "lastName": "Author",
        }

        with allure.step("Send PUT request to /Authors/999"):
            response = api_context.put("/api/v1/Authors/999", data=updated_payload)

        with allure.step("Verify status code is 200"):
            assert response.status == 200

        with allure.step("Verify response body reflects updates"):
            data = response.json()
            assert data["firstName"] == "Updated"
            assert data["lastName"] == "Author"

    @allure.title("DELETE an author returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    def test_delete_author(self, api_context):
        with allure.step("Send DELETE request to /Authors/999"):
            response = api_context.delete("/api/v1/Authors/999")

        with allure.step("Verify status code is 200"):
            assert response.status == 200
