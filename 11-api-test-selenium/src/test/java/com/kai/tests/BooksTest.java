package com.kai.tests;

import io.qameta.allure.*;
import org.testng.annotations.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

@Epic("API Testing")
@Feature("Books API")
public class BooksTest extends BaseTest {

    private static final String BASE_ENDPOINT = "/Books";

    @Test(priority = 1)
    @Story("Read Books")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get all books and verify response is array with data")
    public void getAllBooks() {
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
    @Story("Read Books")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get book by ID and verify properties exist")
    public void getBookById() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("title", notNullValue())
            .body("pageCount", notNullValue());
    }

    @Test(priority = 3)
    @Story("Read Books")
    @Severity(SeverityLevel.NORMAL)
    @Description("GET - Non-existent book returns 404")
    public void getNonExistentBook() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/99999")
        .then()
            .statusCode(404);
    }

    @Test(priority = 4)
    @Story("Create Book")
    @Severity(SeverityLevel.CRITICAL)
    @Description("POST - Create a new book and verify response body matches")
    public void createNewBook() {
        Map<String, Object> body = new HashMap<>();
        body.put("id", testData.get("book").get("id").asInt());
        body.put("title", testData.get("book").get("title").asText());
        body.put("description", testData.get("book").get("description").asText());
        body.put("pageCount", testData.get("book").get("pageCount").asInt());
        body.put("excerpt", testData.get("book").get("excerpt").asText());
        body.put("publishDate", testData.get("book").get("publishDate").asText());

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .post(BASE_ENDPOINT)
        .then()
            .statusCode(200)
            .body("id", equalTo(testData.get("book").get("id").asInt()))
            .body("title", equalTo(testData.get("book").get("title").asText()))
            .body("pageCount", equalTo(testData.get("book").get("pageCount").asInt()));
    }

    @Test(priority = 5)
    @Story("Update Book")
    @Severity(SeverityLevel.CRITICAL)
    @Description("PUT - Update an existing book and verify updated fields")
    public void updateBook() {
        int id = testData.get("book").get("id").asInt();

        Map<String, Object> body = new HashMap<>();
        body.put("id", id);
        body.put("title", "Updated Book");
        body.put("description", testData.get("book").get("description").asText());
        body.put("pageCount", 500);
        body.put("excerpt", testData.get("book").get("excerpt").asText());
        body.put("publishDate", testData.get("book").get("publishDate").asText());

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .put(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200)
            .body("title", equalTo("Updated Book"))
            .body("pageCount", equalTo(500));
    }

    @Test(priority = 6)
    @Story("Delete Book")
    @Severity(SeverityLevel.CRITICAL)
    @Description("DELETE - Delete a book and verify 200 response")
    public void deleteBook() {
        int id = testData.get("book").get("id").asInt();

        given()
            .spec(requestSpec)
        .when()
            .delete(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200);
    }
}
