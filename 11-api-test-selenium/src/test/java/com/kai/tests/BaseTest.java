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
import java.util.Properties;

public class BaseTest {

    protected static JsonNode testData;
    protected static Properties config;
    protected RequestSpecification requestSpec;

    @BeforeSuite
    public void loadTestData() throws Exception {
        // Load config
        config = new Properties();
        InputStream configStream = getClass().getClassLoader().getResourceAsStream("config.properties");
        if (configStream == null) {
            throw new IllegalStateException("config.properties not found in classpath");
        }
        config.load(configStream);

        // Load test data
        ObjectMapper mapper = new ObjectMapper();
        InputStream is = getClass().getClassLoader().getResourceAsStream("testData.json");
        if (is == null) {
            throw new IllegalStateException("testData.json not found in classpath");
        }
        testData = mapper.readTree(is);
    }

    @BeforeClass
    public void setup() {
        RestAssured.baseURI = config.getProperty("base.url");

        requestSpec = new RequestSpecBuilder()
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .addFilter(new AllureRestAssured())
                .build();
    }
}
