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
    getSearchResult: function (searchQuery) {
      return $http.get('http://localhost/api/search/?query=' + searchQuery);
    },
    getRecentlyUpdated: function () {
      return $http.get('http://localhost/api/recent/?count=5');
    }
  };
}]);


angular.module('g4seApp')
  .controller('SearchCtrl',['$scope', '$http', 'dataService', '$timeout', function($scope, $http, dataService, $timeout) {

    $scope.isHidden = true;

    dataService.getRecentlyUpdated().then(function (result) {
      $scope.recentRecords = result.data;
    });

    $scope.enterSearch = function() {
      if ($scope.text){
        dataService.getSearchResult($scope.text).then(function (result) {
          $scope.records = result.data;
          $scope.resultCount = result.data.length;
          $timeout(function () {
            $scope.$apply();
          });
        });
      }
    };

    $scope.expand = function (index) {
      $scope.records[index.$index].detailsHidden = !$scope.records[index.$index].detailsHidden;
      $scope.isHidden = !$scope.isHidden;
      $timeout(function () {
        $scope.$apply();
      });
    };
  }]);
