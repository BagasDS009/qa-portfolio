/**
 * PassengerPage Page Object - KAI Booking
 * XPath locators identical to Playwright passenger_page.py
 */
class PassengerPage {
  // Same XPaths as 01-web-automation-playwright/pages/passenger_page.py
  xpaths = {
    // Contact Person
    contactName: "//input[@id='pemesan_nama' and @name='pemesan_nama']",
    contactPhone: "//input[@id='pemesan_nohp' and @name='pemesan_nohp']",
    contactEmail: "//input[@id='pemesan_email' and @name='pemesan_email']",
    contactIdNumber: "//input[@id='pemesan_notandapengenal']",
    // Passenger
    passengerName: "//input[@id='penumpang_nama1' and @name='penumpang_nama[]']",
    passengerIdNumber: "//input[@id='penumpang_notandapengenal1' and @name='penumpang_notandapengenal[]']",
    // Actions
    continueButton: "//button[@id='bayar' and @name='submitbutton']",
    // Validation errors
    errorMohonIsiNama: "//li[normalize-space()='Mohon isi Nama']",
    errorMohonIsiNoId: "//li[normalize-space()='Mohon isi Nomor Identitas']",
    errorMohonIsiEmail: "//li[normalize-space()='Mohon diisi Email']",
    errorPassengerNoId: "//li[normalize-space()='Nomor Identitas Wajib Diisi']",
  };

  isFormDisplayed() {
    cy.xpath(this.xpaths.contactName).should('be.visible');
  }

  isSubmitButtonDisabled() {
    cy.xpath(this.xpaths.continueButton).should('be.disabled');
  }

  // Blur validation helpers: click field → leave empty → click another field
  triggerBlurName() {
    cy.xpath(this.xpaths.contactName).click();
    cy.wait(500);
    cy.xpath(this.xpaths.contactPhone).click();
    cy.wait(500);
  }

  triggerBlurIdNumber() {
    cy.xpath(this.xpaths.contactIdNumber).click();
    cy.wait(500);
    cy.xpath(this.xpaths.contactName).click();
    cy.wait(500);
  }

  triggerBlurEmail() {
    cy.xpath(this.xpaths.contactEmail).click();
    cy.wait(500);
    cy.xpath(this.xpaths.contactName).click();
    cy.wait(500);
  }

  triggerBlurPassengerId() {
    cy.xpath(this.xpaths.passengerIdNumber).click();
    cy.wait(500);
    cy.xpath(this.xpaths.passengerName).click();
    cy.wait(500);
  }

  verifyErrorMohonIsiNama() {
    cy.xpath(this.xpaths.errorMohonIsiNama).should('be.visible');
  }

  verifyErrorMohonIsiNoId() {
    cy.xpath(this.xpaths.errorMohonIsiNoId).should('be.visible');
  }

  verifyErrorMohonIsiEmail() {
    cy.xpath(this.xpaths.errorMohonIsiEmail).should('be.visible');
  }

  verifyErrorPassengerNoId() {
    cy.xpath(this.xpaths.errorPassengerNoId).should('be.visible');
  }

  verifyPassengerNameRequired() {
    cy.xpath(this.xpaths.passengerName).should('have.attr', 'required');
  }
}

export default new PassengerPage();
