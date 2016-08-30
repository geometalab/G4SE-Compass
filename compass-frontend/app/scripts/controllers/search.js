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
    },
    getRecentlyUpdated: function () {
      return $http.get('http://localhost/api/recent/?count=5');
    }
  }
}]);


angular.module('g4seApp')
  .controller('SearchCtrl',['$scope', '$http', 'dataService', '$timeout', function($scope, $http, dataService, $timeout) {
    dataService.getRecentlyUpdated().then(function (result) {
      $scope.recent_records = result.data;
    });

    $scope.enter_search = function() {
      console.log('hi');
      if ($scope.text){
        dataService.getSearchResult($scope.text).then(function (result) {
          $scope.records = result.data;
          $scope.result_count = result.data.length;
          $timeout(function () {
            $scope.$apply()
          })
        });
      }
    };
  }]);
