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
      return $http.get('http://localhost/api/search/?query=' + encodeURIComponent(searchQuery));
    },
    getSingleResult: function (id) {
      return $http.get('http://localhost/api/metadata/' + id);
    },
    getRecentlyUpdated: function () {
      return $http.get('http://localhost/api/recent/?count=5');
    }
  };
}]);


angular.module('g4seApp')
  .controller('SearchCtrl',['$scope', '$http', 'dataService', '$timeout', function($scope, $http, dataService, $timeout) {
    $scope.itemsPerPage = 5;

    $scope.setPage = function (pageNo) {
      $scope.currentPage = pageNo;
    };

    $scope.pageChanged = function() {
      $scope.begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
      $scope.end = $scope.begin + $scope.itemsPerPage;
      $scope.filteredRecords = $scope.records.slice($scope.begin, $scope.end);
      $timeout(function () {
        $scope.$apply();
      });
    };

    dataService.getRecentlyUpdated().then(function (result) {
      $scope.recentRecords = result.data;
    });

    $scope.singleResult = function(apiId) {
      dataService.getSingleResult(apiId).then(function (result) {
        $scope.filteredRecords = [result.data];
        $scope.totalItems = null;
        $timeout(function () {
          $scope.$apply();
        });
      });
    };

    $scope.enterSearch = function() {
      if ($scope.text){
        dataService.getSearchResult($scope.text).then(function (result) {
          $scope.records = result.data;
          $scope.totalItems = result.data.length;
          $scope.setPage(1);
          $scope.pageChanged();
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
