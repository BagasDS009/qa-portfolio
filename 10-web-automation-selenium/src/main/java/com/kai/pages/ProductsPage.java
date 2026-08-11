package com.kai.pages;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import io.qameta.allure.Step;
import java.util.List;

public class ProductsPage extends BasePage {
    private final By allProductsTitle = By.xpath("//h2[contains(text(),'All Products') or contains(text(),'ALL PRODUCTS')]");
    private final By productsList = By.cssSelector(".features_items .col-sm-4");
    private final By firstViewProduct = By.cssSelector("a[href='/product_details/1']");
    private final By searchInput = By.id("search_product");
    private final By searchBtn = By.id("submit_search");
    private final By searchedProductsTitle = By.xpath("//h2[contains(text(),'Searched Products')]");
    private final By productName = By.cssSelector(".productinfo p");
    private final By addToCartBtns = By.cssSelector(".add-to-cart");

    // Product detail page
    private final By detailName = By.cssSelector(".product-information h2");
    private final By detailCategory = By.xpath("//p[contains(text(),'Category')]");
    private final By detailPrice = By.cssSelector(".product-information span span");
    private final By detailAvailability = By.xpath("//p[contains(text(),'Availability')]");
    private final By detailCondition = By.xpath("//p[contains(text(),'Condition')]");
    private final By detailBrand = By.xpath("//p[contains(text(),'Brand')]");

    public ProductsPage(WebDriver driver) {
        super(driver);
    }

    public boolean isAllProductsVisible() {
        return isVisible(allProductsTitle);
    }

    public int getProductCount() {
        return driver.findElements(productsList).size();
    }

    @Step("Click View Product of first product")
    public void viewFirstProduct() {
        driver.get(BASE_URL + "/product_details/1");
    }

    @Step("Search product: {keyword}")
    public void searchProduct(String keyword) {
        type(searchInput, keyword);
        click(searchBtn);
    }

    public boolean isSearchedProductsVisible() {
        return isVisible(searchedProductsTitle);
    }

    public boolean isProductDetailVisible() {
        return isVisible(detailName) || isVisible(detailPrice);
    }

    @Step("Add first product to cart")
    public void addFirstProductToCart() {
        List<WebElement> btns = driver.findElements(addToCartBtns);
        if (!btns.isEmpty()) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btns.get(0));
        }
    }
}
