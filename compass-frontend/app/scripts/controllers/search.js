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
      return $http.get(API_BASE_URL + '/api/metadata/search/?query=' + encodeURIComponent(searchQuery));
    },
    getSingleResult: function (id) {
      return $http.get(API_BASE_URL + '/api/metadata/' + id + '/');
    },
    getRecentlyUpdated: function () {
      return $http.get(API_BASE_URL + '/api/metadata/recent/?count=5');
    }
  };
}]);


angular.module('g4seApp')
  .filter('linkify', ['$sanitize', function($sanitize) {
    var LINKY_URL_REGEXP =
        /((ftp|https?):\/\/|(www\.)|(mailto:)?[A-Za-z0-9._%+-]+@)\S*[^\s.;,(){}<>"\u201d\u2019]/i,
      MAILTO_REGEXP = /^mailto:/i;

    var linkyMinErr = angular.$$minErr('linkify');
    var isString = angular.isString;

    return function(text, limit) {
      if (text == null || text === '') return text;
      if (!isString(text)) throw linkyMinErr('notstring', 'Expected string but received: {0}', text);

      if ((limit == null) || (limit == undefined)) limit = 20000;
      if (limit < 20) limit = 20;

      var match;
      var raw = text;
      var html = [];
      var url;
      var i;
      while ((match = raw.match(LINKY_URL_REGEXP))) {
        // We can not end in these as they are sometimes found at the end of the sentence
        url = match[0];
        // if we did not match ftp/http/www/mailto then assume mailto
        if (!match[2] && !match[4]) {
          url = (match[3] ? 'http://' : 'mailto:') + url;
        }
        i = match.index;
        addText(raw.substr(0, i));
        addLink(url, match[0].replace(MAILTO_REGEXP, ''));
        raw = raw.substring(i + match[0].length);
      }
      addText(raw);
      return $sanitize(html.join(''));

      function addText(text) {
        if (!text) {
          return;
        }
        html.push($sanitize(text));
      }

      function addLink(url, text) {
        html.push('<a ');

        html.push('href="',
          url.replace(/"/g, '&quot;'),
          '">');
        if (text.length > limit) {
          addText(text.slice(0, 10));
          addText('...');
          addText(text.slice(text.length - (limit - 13), text.length));
        } else {
          addText(text);
        }
        html.push('</a>');
      }
    };
  }])
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
        $scope.text = null;
        dataService.getSingleResult(apiId).then(function (result) {
          var record = result.data;
          record.showDetails = true;
          $scope.filteredRecords = [record];
          console.log(record);
          // null so pagination section isn't shown
          $scope.totalItems = null;
          $location.search('id', result.data['api_id']);
          $timeout(function () {
            $scope.$apply();
          });
        }, function errorCallback(response) {
          // TODO error handling
        });
      };

      $scope.enterSearch = function() {
        if ($scope.text){
          $location.search('id', null);
          dataService.getSearchResult($scope.text).then(function (result) {
            $scope.records = result.data;
            $scope.totalItems = result.data.length;
            $scope.setPage(1);
            $scope.pageChanged();
          });
        }
      };

      $scope.expand = function (index) {
        $scope.filteredRecords[index.$index].showDetails = !$scope.filteredRecords[index.$index].showDetails;
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
