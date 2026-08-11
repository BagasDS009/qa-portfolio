package com.kai.pages;

import org.openqa.selenium.*;
import io.qameta.allure.Step;

public class LoginPage extends BasePage {
    private final By newUserSignupText = By.xpath("//h2[text()='New User Signup!']");
    private final By loginText = By.xpath("//h2[text()='Login to your account']");
    private final By signupName = By.cssSelector("input[data-qa='signup-name']");
    private final By signupEmail = By.cssSelector("input[data-qa='signup-email']");
    private final By signupBtn = By.cssSelector("button[data-qa='signup-button']");
    private final By loginEmail = By.cssSelector("input[data-qa='login-email']");
    private final By loginPassword = By.cssSelector("input[data-qa='login-password']");
    private final By loginBtn = By.cssSelector("button[data-qa='login-button']");
    private final By loginError = By.xpath("//p[contains(text(),'incorrect')]");
    private final By signupError = By.xpath("//p[contains(text(),'already exist')]");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public boolean isNewUserSignupVisible() {
        return isVisible(newUserSignupText);
    }

    public boolean isLoginFormVisible() {
        return isVisible(loginText);
    }

    @Step("Signup with name: {name}, email: {email}")
    public void signup(String name, String email) {
        type(signupName, name);
        type(signupEmail, email);
        WebElement btn = driver.findElement(signupBtn);
        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
    }

    @Step("Login with email: {email}")
    public void login(String email, String password) {
        type(loginEmail, email);
        type(loginPassword, password);
        WebElement btn = driver.findElement(loginBtn);
        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
    }

    public boolean isLoginErrorVisible() {
        return isVisible(loginError);
    }

    public boolean isSignupErrorVisible() {
        return isVisible(signupError);
    }
}
