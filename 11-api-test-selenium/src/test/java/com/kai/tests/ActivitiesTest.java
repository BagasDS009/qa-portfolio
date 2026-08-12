package com.kai.tests;

import io.qameta.allure.*;
import org.testng.annotations.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

@Epic("API Testing")
@Feature("Activities API")
public class ActivitiesTest extends BaseTest {

    private static final String BASE_ENDPOINT = "/Activities";

    @Test(priority = 1)
    @Story("Read Activities")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get all activities and verify response is array with data")
    public void getAllActivities() {
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
    @Story("Read Activities")
    @Severity(SeverityLevel.CRITICAL)
    @Description("GET - Get activity by ID and verify properties exist")
    public void getActivityById() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("title", notNullValue())
            .body("dueDate", notNullValue())
            .body("completed", notNullValue());
    }

    @Test(priority = 3)
    @Story("Read Activities")
    @Severity(SeverityLevel.NORMAL)
    @Description("GET - Non-existent activity returns 404")
    public void getNonExistentActivity() {
        given()
            .spec(requestSpec)
        .when()
            .get(BASE_ENDPOINT + "/99999")
        .then()
            .statusCode(404);
    }

    @Test(priority = 4)
    @Story("Create Activity")
    @Severity(SeverityLevel.CRITICAL)
    @Description("POST - Create a new activity and verify response body matches")
    public void createNewActivity() {
        Map<String, Object> body = new HashMap<>();
        body.put("id", testData.get("activity").get("id").asInt());
        body.put("title", testData.get("activity").get("title").asText());
        body.put("dueDate", testData.get("activity").get("dueDate").asText());
        body.put("completed", testData.get("activity").get("completed").asBoolean());

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .post(BASE_ENDPOINT)
        .then()
            .statusCode(200)
            .body("id", equalTo(testData.get("activity").get("id").asInt()))
            .body("title", equalTo(testData.get("activity").get("title").asText()))
            .body("completed", equalTo(testData.get("activity").get("completed").asBoolean()));
    }

    @Test(priority = 5)
    @Story("Update Activity")
    @Severity(SeverityLevel.CRITICAL)
    @Description("PUT - Update an existing activity and verify updated fields")
    public void updateActivity() {
        int id = testData.get("activity").get("id").asInt();

        Map<String, Object> body = new HashMap<>();
        body.put("id", id);
        body.put("title", "Updated Activity");
        body.put("dueDate", testData.get("activity").get("dueDate").asText());
        body.put("completed", true);

        given()
            .spec(requestSpec)
            .body(body)
        .when()
            .put(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200)
            .body("title", equalTo("Updated Activity"))
            .body("completed", equalTo(true));
    }

    @Test(priority = 6)
    @Story("Delete Activity")
    @Severity(SeverityLevel.CRITICAL)
    @Description("DELETE - Delete an activity and verify 200 response")
    public void deleteActivity() {
        int id = testData.get("activity").get("id").asInt();

        given()
            .spec(requestSpec)
        .when()
            .delete(BASE_ENDPOINT + "/" + id)
        .then()
            .statusCode(200);
    }
}
