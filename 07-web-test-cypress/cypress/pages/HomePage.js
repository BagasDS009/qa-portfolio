/**
 * HomePage Page Object - KAI Booking
 * XPath locators identical to Playwright home_page.py
 */
class HomePage {
  // Same XPaths as 01-web-automation-playwright/pages/home_page.py
  xpaths = {
    originInput: '//input[@placeholder="Stasiun Asal..." and @id="origination-flexdatalist"]',
    destinationInput: '//input[@placeholder="Stasiun Tujuan..." and @id="destination-flexdatalist"]',
    departureDate: '//input[@data-error="Mohon diisi tanggal" and @name="tanggal"]',
    datepickerNextMonth: '//a[@class="ui-datepicker-next ui-corner-all" and @data-event="click" and @title="Next"]',
    datepickerPrevMonth: '//a[@class="ui-datepicker-prev ui-corner-all" and @data-event="click" and @title="Prev"]',
    adultMinus: '//button[@data-type="minus" and @data-field="dewasa"]',
    adultPlus: '//button[@data-type="plus" and @data-field="dewasa"]',
    adultCount: '//input[@id="dewasa"]',
    babyMinus: '//button[@data-type="minus" and @data-field="infant"]',
    babyPlus: '//button[@data-type="plus" and @data-field="infant"]',
    babyCount: '//input[@id="infant"]',
    babyTooltip: '//span[@class="tooltiptext"]',
    searchButton: '//input[@id="submit"]',
  };

  visit() {
    cy.visit('/', { failOnStatusCode: false, timeout: 60000 });
    cy.wait(5000);
  }

  selectOriginStation(station) {
    cy.xpath(this.xpaths.originInput).click({ force: true });
    cy.wait(500);
    cy.xpath(this.xpaths.originInput).clear({ force: true });
    cy.xpath(this.xpaths.originInput).type(station, { delay: 150, force: true })
      .trigger('input')
      .trigger('keyup');
    cy.wait(2500);
    // Click matching station from dropdown
    cy.xpath(`//span[text()="${station}"]`).click({ force: true });
    cy.wait(500);
  }

  selectDestinationStation(station) {
    cy.xpath(this.xpaths.destinationInput).click({ force: true });
    cy.wait(500);
    cy.xpath(this.xpaths.destinationInput).clear({ force: true });
    cy.xpath(this.xpaths.destinationInput).type(station, { delay: 150, force: true })
      .trigger('input')
      .trigger('keyup');
    cy.wait(2500);
    // Click matching station from dropdown
    cy.xpath(`//span[text()="${station}"]`).click({ force: true });
    cy.wait(500);
  }

  setDepartureDate(tgl) {
    cy.xpath(this.xpaths.departureDate).click();
    cy.wait(800);
    cy.xpath(this.xpaths.datepickerNextMonth).click();
    cy.wait(500);
    cy.xpath(`//a[@class="ui-state-default" and normalize-space()="${tgl}"]`).click();
    cy.wait(500);
  }

  setAdultCount(count) {
    for (let i = 1; i < count; i++) {
      cy.xpath(this.xpaths.adultPlus).click();
      cy.wait(300);
    }
  }

  setBabyCount(count) {
    for (let i = 0; i < count; i++) {
      cy.xpath(this.xpaths.babyPlus).click();
      cy.wait(300);
    }
  }

  clickSearch() {
    cy.xpath(this.xpaths.searchButton).click({ force: true });
    cy.wait(3000);
  }

  searchTrain(origin, destination, tgl, adults = 1, babies = 0) {
    this.selectOriginStation(origin);
    this.selectDestinationStation(destination);
    this.setDepartureDate(tgl);
    if (adults > 1) this.setAdultCount(adults);
    if (babies > 0) this.setBabyCount(babies);
    this.clickSearch();
  }

  isSearchFormVisible() {
    cy.xpath(this.xpaths.originInput).should('be.visible');
    cy.xpath(this.xpaths.destinationInput).should('be.visible');
  }

  getAdultCount() {
    return cy.xpath(this.xpaths.adultCount).invoke('val');
  }

  clickBabyPlus() {
    cy.xpath(this.xpaths.babyPlus).click({ force: true });
    cy.wait(500);
  }

  getBabyTooltip() {
    return cy.xpath(this.xpaths.babyTooltip);
  }

  isBabyTooltipVisible() {
    // Tooltip might need force-check since it's CSS display:none until triggered
    cy.xpath(this.xpaths.babyTooltip).should('have.css', 'display').and('not.eq', 'none');
  }
}

export default new HomePage();
