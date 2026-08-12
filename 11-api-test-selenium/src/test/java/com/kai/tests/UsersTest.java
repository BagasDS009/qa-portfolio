package com.kai.tests;

import io.qameta.allure.*;
import org.testng.annotations.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

@Epic("API Testing")
@Feature("Users API")
public class UsersTest extends BaseTest {

    private static final String BASE_ENDPOINT = "/Users";

    @Test(priority = 1)
    @Story("Read Users")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get all users and verify response is array with data")
    public void getAllUsers() {
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
    @Story("Read Users")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get user by ID and verify properties exist")
    public void getUserById() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("userName", notNullValue())
            .body("password", notNullValue());
    }

    @Test(priority = 3)
    @Story("Read Users")
    @Severity(SeverityLevel.NORMAL)
    @Description("GET - Non-existent user returns 404")
    public void getNonExistentUser() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/99999")
        .then()
            .statusCode(404);
    }

    @Test(priority = 4)
    @Story("Create User")
    @Severity(SeverityLevel.CRITICAL)
    @Description("POST - Create a new user and verify response body matches")
    public void createNewUser() {
        Map<String, Object> body = new HashMap<>();
        body.put("id", testData.get("user").get("id").asInt());
        body.put("userName", testData.get("user").get("userName").asText());
        body.put("password", testData.get("user").get("password").asText());

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .post(BASE_ENDPOINT)
        .then()
            .statusCode(200)
            .body("id", equalTo(testData.get("user").get("id").asInt()))
            .body("userName", equalTo(testData.get("user").get("userName").asText()))
            .body("password", equalTo(testData.get("user").get("password").asText()));
    }

    @Test(priority = 5)
    @Story("Update User")
    @Severity(SeverityLevel.CRITICAL)
    @Description("PUT - Update an existing user and verify updated fields")
    public void updateUser() {
        int id = testData.get("user").get("id").asInt();

        Map<String, Object> body = new HashMap<>();
        body.put("id", id);
        body.put("userName", "updateduser");
        body.put("password", "Updated@456");

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .put(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200)
            .body("userName", equalTo("updateduser"))
            .body("password", equalTo("Updated@456"));
    }

    @Test(priority = 6)
    @Story("Delete User")
    @Severity(SeverityLevel.CRITICAL)
    @Description("DELETE - Delete a user and verify 200 response")
    public void deleteUser() {
        int id = testData.get("user").get("id").asInt();

        given()
            .spec(requestSpec)
        .when()
            .delete(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200);
    }
}
