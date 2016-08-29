'use strict';

/**
 * @ngdoc function
 * @name g4seApp.controller:SearchCtrl
 * @description
 * # SearchCtrl
 * Controller of the g4seApp
 */
angular.module('g4seApp').service('dataService', ['$http', function ($http) {
  return {
    getSearchResult: function (search_query) {
      return $http.get('http://localhost/api/search/?query=' + search_query);
    }
  }
}]);


angular.module('g4seApp')
  .controller('SearchCtrl',['$scope', '$http', 'dataService', '$timeout', function($scope, $http, dataService, $timeout) {
    $scope.enter_search = function() {
      if ($scope.text){
        dataService.getSearchResult($scope.text).then(function (result) {
          $scope.records = result.data;
          $timeout(function () {
            $scope.$apply()
          })
        });
      }
    };
  }]);
