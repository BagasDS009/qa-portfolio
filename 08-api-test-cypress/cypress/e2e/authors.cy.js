describe('Authors API - CRUD', () => {
  const baseEndpoint = '/Authors';

  it('GET - Get all authors', () => {
    cy.request('GET', baseEndpoint).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body.length).to.be.greaterThan(0);
    });
  });

  it('GET - Get author by ID', () => {
    cy.request('GET', `${baseEndpoint}/1`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('id', 1);
      expect(response.body).to.have.property('firstName');
      expect(response.body).to.have.property('lastName');
    });
  });

  it('GET - Get authors by book ID', () => {
    cy.request('GET', '/Authors/authors/books/1').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
    });
  });

  it('GET - Non-existent author returns 404', () => {
    cy.request({ method: 'GET', url: `${baseEndpoint}/99999`, failOnStatusCode: false }).then((response) => {
      expect(response.status).to.eq(404);
    });
  });

  it('POST - Create a new author', () => {
    cy.fixture('testData').then((data) => {
      cy.request('POST', baseEndpoint, data.author).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.id).to.eq(data.author.id);
        expect(response.body.firstName).to.eq(data.author.firstName);
        expect(response.body.lastName).to.eq(data.author.lastName);
      });
    });
  });

  it('PUT - Update an existing author', () => {
    cy.fixture('testData').then((data) => {
      const updated = { ...data.author, firstName: 'Updated', lastName: 'Author' };
      cy.request('PUT', `${baseEndpoint}/${data.author.id}`, updated).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.firstName).to.eq('Updated');
        expect(response.body.lastName).to.eq('Author');
      });
    });
  });

  it('DELETE - Delete an author', () => {
    cy.fixture('testData').then((data) => {
      cy.request('DELETE', `${baseEndpoint}/${data.author.id}`).then((response) => {
        expect(response.status).to.eq(200);
      });
    });
  });
});
