'use strict';

describe('Directive: searchDirective', function () {

  // load the directive's module
  beforeEach(module('g4seApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<search-directive></search-directive>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the searchDirective directive');
  }));
});
