package com.kai.tests;

import com.kai.pages.HomePage;
import com.kai.pages.LoginPage;
import io.qameta.allure.*;
import org.testng.Assert;
import org.testng.annotations.*;

@Epic("Automation Exercise")
@Feature("Authentication")
public class LoginTest extends BaseTest {
    private HomePage homePage;
    private LoginPage loginPage;

    @BeforeMethod(dependsOnMethods = "setUp")
    public void initPages() {
        homePage = new HomePage(driver);
        loginPage = new LoginPage(driver);
    }

    // ========================
    // POSITIVE
    // ========================

    @Test(priority = 1)
    @Story("Login")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-04: Verify Login and Signup forms are accessible")
    public void testLoginAndSignupFormsVisible() {
        homePage.open();
        homePage.clickSignupLogin();
        Assert.assertTrue(loginPage.isLoginFormVisible(), "Login form not visible");
        Assert.assertTrue(loginPage.isNewUserSignupVisible(), "Signup form not visible");
    }

    // ========================
    // NEGATIVE - Login
    // ========================

    @Test(priority = 2)
    @Story("Login")
    @Severity(SeverityLevel.CRITICAL)
    @Description("TC-03a: Login with incorrect email and password")
    public void testLoginWithIncorrectCredentials() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.login("invalid@test.com", "wrongpassword");
        Assert.assertTrue(loginPage.isLoginErrorVisible(), "Login error not shown");
    }

    @Test(priority = 3)
    @Story("Login")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-03b: Login with empty email field")
    public void testLoginWithEmptyEmail() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.login("", "somepassword");
        // Should stay on login page (HTML validation or no redirect)
        Assert.assertTrue(loginPage.isLoginFormVisible(), "Should remain on login page");
    }

    @Test(priority = 4)
    @Story("Login")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-03c: Login with empty password field")
    public void testLoginWithEmptyPassword() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.login("test@test.com", "");
        Assert.assertTrue(loginPage.isLoginFormVisible(), "Should remain on login page");
    }

    // ========================
    // NEGATIVE - Signup
    // ========================

    @Test(priority = 5)
    @Story("Signup")
    @Severity(SeverityLevel.CRITICAL)
    @Description("TC-05: Register User with existing email")
    public void testSignupWithExistingEmail() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.signup("TestUser", "existing@test.com");
        Assert.assertTrue(loginPage.isSignupErrorVisible(), "Signup error 'Email already exist' not shown");
    }

    @Test(priority = 6)
    @Story("Signup")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-05b: Signup with empty name field")
    public void testSignupWithEmptyName() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.signup("", "newuser@test.com");
        // Should stay on page (HTML required validation)
        Assert.assertTrue(loginPage.isNewUserSignupVisible(), "Should remain on signup form");
    }

    @Test(priority = 7)
    @Story("Signup")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-05c: Signup with empty email field")
    public void testSignupWithEmptyEmail() {
        homePage.open();
        homePage.clickSignupLogin();
        loginPage.signup("TestUser", "");
        Assert.assertTrue(loginPage.isNewUserSignupVisible(), "Should remain on signup form");
    }
}
