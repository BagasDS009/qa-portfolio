package com.kai.tests;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.qameta.allure.restassured.AllureRestAssured;
import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeSuite;

import java.io.InputStream;

public class BaseTest {

    protected static JsonNode testData;
    protected RequestSpecification requestSpec;

    @BeforeSuite
    public void loadTestData() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        InputStream is = getClass().getClassLoader().getResourceAsStream("testData.json");
        testData = mapper.readTree(is);
    }

    @BeforeClass
    public void setup() {
        RestAssured.baseURI = "https://fakerestapi.azurewebsites.net/api/v1";

        requestSpec = new RequestSpecBuilder()
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .addFilter(new AllureRestAssured())
                .build();
    }
}
