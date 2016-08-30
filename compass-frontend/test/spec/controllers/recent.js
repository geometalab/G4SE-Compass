'use strict';

describe('Controller: RecentCtrl', function () {

  // load the controller's module
  beforeEach(module('g4seApp'));

  var RecentCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    RecentCtrl = $controller('RecentCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(RecentCtrl.awesomeThings.length).toBe(3);
  });
});
