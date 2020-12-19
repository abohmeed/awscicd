var app = require('../index'), request = require('supertest');

describe('Ensure that the correct response is received', function(){
  describe('when requesting resource /', function(){
    it('should respond with 200 and JSON content type', function(done){
      request(app)
      .get('/')
      .expect('Content-Type', /json/)
      .expect(200, done);
    });
  });
});
