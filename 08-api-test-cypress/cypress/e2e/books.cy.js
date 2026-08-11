describe('Books API - CRUD', () => {
  const baseEndpoint = '/Books';

  it('GET - Get all books', () => {
    cy.request('GET', baseEndpoint).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body.length).to.be.greaterThan(0);
    });
  });

  it('GET - Get book by ID', () => {
    cy.request('GET', `${baseEndpoint}/1`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('id', 1);
      expect(response.body).to.have.property('title');
      expect(response.body).to.have.property('pageCount');
    });
  });

  it('GET - Non-existent book returns 404', () => {
    cy.request({ method: 'GET', url: `${baseEndpoint}/99999`, failOnStatusCode: false }).then((response) => {
      expect(response.status).to.eq(404);
    });
  });

  it('POST - Create a new book', () => {
    cy.fixture('testData').then((data) => {
      cy.request('POST', baseEndpoint, data.book).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.id).to.eq(data.book.id);
        expect(response.body.title).to.eq(data.book.title);
        expect(response.body.pageCount).to.eq(data.book.pageCount);
      });
    });
  });

  it('PUT - Update an existing book', () => {
    cy.fixture('testData').then((data) => {
      const updated = { ...data.book, title: 'Updated Book', pageCount: 500 };
      cy.request('PUT', `${baseEndpoint}/${data.book.id}`, updated).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.title).to.eq('Updated Book');
        expect(response.body.pageCount).to.eq(500);
      });
    });
  });

  it('DELETE - Delete a book', () => {
    cy.fixture('testData').then((data) => {
      cy.request('DELETE', `${baseEndpoint}/${data.book.id}`).then((response) => {
        expect(response.status).to.eq(200);
      });
    });
  });
});
