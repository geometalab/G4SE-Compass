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
  .controller('SearchCtrl',['$scope', '$http', 'dataService', '$timeout', '$window', '$routeParams', '$location',
    function ($scope, $http, dataService, $timeout, $window, $routeParams, $location) {
      $scope.itemsPerPage = 10;
      $scope.setPage = function (pageNo) {
        $scope.currentPage = pageNo;
      };

      $scope.pageChanged = function() {
        $scope.begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
        $scope.end = $scope.begin + $scope.itemsPerPage;
        $scope.filteredRecords = $scope.records.slice($scope.begin, $scope.end);
        $window.scrollTo(0, 0);
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
          // null so pagination section isn't shown
          $scope.totalItems = null;
          $location.search('id', result.data['api_id']);
          $timeout(function () {
            $scope.$apply();
          });
        }, function errorCallback(response) {
          if(response.status == 404){
            console.log(response);
          }else{

          }
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
        $scope.filteredRecords[index.$index].detailsHidden = !$scope.filteredRecords[index.$index].detailsHidden;
        $location.search('id', $scope.filteredRecords[index.$index]['api_id']);
        $scope.isHidden = !$scope.isHidden;
        $timeout(function () {
          $scope.$apply();
        });
      };

      if($routeParams['id']){
        $scope.singleResult($routeParams['id'])
      }
    }
  ]);
