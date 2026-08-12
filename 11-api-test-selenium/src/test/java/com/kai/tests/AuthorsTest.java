package com.kai.tests;

import io.qameta.allure.*;
import org.testng.annotations.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

@Epic("API Testing")
@Feature("Authors API")
public class AuthorsTest extends BaseTest {

    private static final String BASE_ENDPOINT = "/Authors";

    @Test(priority = 1)
    @Story("Read Authors")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get all authors and verify response is array with data")
    public void getAllAuthors() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT)
        .then()
            .statusCode(200)
            .body("$", instanceOf(java.util.List.class))
            .body("size()", greaterThan(0));
    }

    @Test(priority = 2)
    @Story("Read Authors")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get author by ID and verify properties exist")
    public void getAuthorById() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("firstName", notNullValue())
            .body("lastName", notNullValue());
    }

    @Test(priority = 3)
    @Story("Read Authors")
    @Severity(SeverityLevel.NORMAL)
    @Description("GET - Get authors by book ID and verify response is array")
    public void getAuthorsByBookId() {
        given()
            .spec(requestSpec)
        .when()
            .get("/Authors/authors/books/1")
        .then()
            .statusCode(200)
            .body("$", instanceOf(java.util.List.class));
    }

    @Test(priority = 4)
    @Story("Read Authors")
    @Severity(SeverityLevel.NORMAL)
    @Description("GET - Non-existent author returns 404")
    public void getNonExistentAuthor() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/99999")
        .then()
            .statusCode(404);
    }

    @Test(priority = 5)
    @Story("Create Author")
    @Severity(SeverityLevel.CRITICAL)
    @Description("POST - Create a new author and verify response body matches")
    public void createNewAuthor() {
        Map<String, Object> body = new HashMap<>();
        body.put("id", testData.get("author").get("id").asInt());
        body.put("idBook", testData.get("author").get("idBook").asInt());
        body.put("firstName", testData.get("author").get("firstName").asText());
        body.put("lastName", testData.get("author").get("lastName").asText());

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .post(BASE_ENDPOINT)
        .then()
            .statusCode(200)
            .body("id", equalTo(testData.get("author").get("id").asInt()))
            .body("firstName", equalTo(testData.get("author").get("firstName").asText()))
            .body("lastName", equalTo(testData.get("author").get("lastName").asText()));
    }

    @Test(priority = 6)
    @Story("Update Author")
    @Severity(SeverityLevel.CRITICAL)
    @Description("PUT - Update an existing author and verify updated fields")
    public void updateAuthor() {
        int id = testData.get("author").get("id").asInt();

        Map<String, Object> body = new HashMap<>();
        body.put("id", id);
        body.put("idBook", testData.get("author").get("idBook").asInt());
        body.put("firstName", "Updated");
        body.put("lastName", "Author");

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .put(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200)
            .body("firstName", equalTo("Updated"))
            .body("lastName", equalTo("Author"));
    }

    @Test(priority = 7)
    @Story("Delete Author")
    @Severity(SeverityLevel.CRITICAL)
    @Description("DELETE - Delete an author and verify 200 response")
    public void deleteAuthor() {
        int id = testData.get("author").get("id").asInt();

        given()
            .spec(requestSpec)
        .when()
            .delete(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200);
    }
}
