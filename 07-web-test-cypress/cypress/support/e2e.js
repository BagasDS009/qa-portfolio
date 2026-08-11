import './commands';
import '@cypress/xpath';

// Ignore uncaught exceptions from the application
Cypress.on('uncaught:exception', (err, runnable) => {
  return false;
});
