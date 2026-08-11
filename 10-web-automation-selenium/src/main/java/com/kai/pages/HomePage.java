package com.kai.pages;

import org.openqa.selenium.*;
import io.qameta.allure.Step;

public class HomePage extends BasePage {
    private final By signupLoginBtn = By.cssSelector("a[href='/login']");
    private final By loggedInAs = By.cssSelector("a:has(i.fa-user)");
    private final By deleteAccountBtn = By.cssSelector("a[href='/delete_account']");
    private final By productsBtn = By.cssSelector("a[href='/products']");
    private final By cartBtn = By.cssSelector("a[href='/view_cart']");
    private final By contactUsBtn = By.cssSelector("a[href='/contact_us']");
    private final By subscriptionText = By.xpath("//h2[text()='Subscription']");
    private final By subscriptionEmail = By.id("susbscribe_email");
    private final By subscriptionBtn = By.id("subscribe");
    private final By subscriptionSuccess = By.xpath("//*[contains(text(),'successfully subscribed')]");
    private final By slider = By.cssSelector(".carousel-inner .item.active");

    public HomePage(WebDriver driver) {
        super(driver);
    }

    @Step("Navigate to home page")
    public void open() {
        navigate();
    }

    public boolean isHomePageVisible() {
        return isVisible(slider);
    }

    @Step("Click Signup/Login button")
    public void clickSignupLogin() {
        click(signupLoginBtn);
    }

    public boolean isLoggedInAs(String username) {
        return getText(loggedInAs).contains(username);
    }

    @Step("Click Delete Account")
    public void clickDeleteAccount() {
        click(deleteAccountBtn);
    }

    @Step("Click Products button")
    public void clickProducts() {
        click(productsBtn);
    }

    @Step("Click Cart button")
    public void clickCart() {
        click(cartBtn);
    }

    @Step("Click Contact Us button")
    public void clickContactUs() {
        click(contactUsBtn);
    }

    @Step("Subscribe with email: {email}")
    public void subscribe(String email) {
        scrollTo(subscriptionText);
        type(subscriptionEmail, email);
        click(subscriptionBtn);
    }

    public boolean isSubscriptionSuccess() {
        return isVisible(subscriptionSuccess);
    }
}
