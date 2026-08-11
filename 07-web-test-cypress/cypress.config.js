const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://booking.kai.id',
    viewportWidth: 1366,
    viewportHeight: 768,
    defaultCommandTimeout: 30000,
    pageLoadTimeout: 60000,
    video: true,
    screenshotOnRunFailure: true,
    testIsolation: true,
    setupNodeEvents(on, config) {
      return config;
    },
  },
});
