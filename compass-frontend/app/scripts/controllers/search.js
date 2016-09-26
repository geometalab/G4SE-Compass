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
    getRecords: function (language, page_size, page, searchQuery) {
      if (page === undefined){
        page = 1;
      }
      if (page_size === undefined){
        page_size = 10;
      }
      if (language === undefined){
        language = 'de';
      }
      if (searchQuery === undefined) {
        searchQuery = '';
      } else {
        searchQuery = '&search=' + encodeURIComponent(searchQuery);
      }
      language = '?language=' + language;
      page_size = '&page_size=' + page_size;
      page = '&page=' + page;
      return $http.get(API_BASE_URL + '/api/metadata/' + language + page_size + page + searchQuery);
    },
    getRecord: function (id) {
      return $http.get(API_BASE_URL + '/api/metadata/' + id + '/');
    },
    getRecentRecords: function () {
      return $http.get(API_BASE_URL + '/api/metadata/?limit=5&ordering=-modified');
    },
    getResults: function (url) {
      if (!API_BASE_URL in url) {
        return null;
      }
      return $http.get(url);
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
      $scope.showSpinner = false;
      $scope.itemsPerPage = 10;

      dataService.getRecentRecords().then(function (result) {
        $scope.recentRecords = result.data["results"];
      });

      function recordsChanged(result){
        $scope.records = result.data["results"];
        $scope.totalItems = result.data["count"];
        if ($scope.currentPage === undefined) {
          $scope.currentPage = 1;
        }
        $scope.showSpinner = false;
        $timeout(function () {
          $scope.$apply();
        })
      }

      if ($scope.language == undefined) {
        $scope.language = 'de';
      }

      if ($scope.records === undefined){
        $scope.showSpinner = true;
        dataService.getRecords($scope.language, $scope.itemsPerPage, $scope.currentPage, $scope.text).then(recordsChanged);
      }

      $scope.setPage = function (pageNo) {
        $scope.currentPage = pageNo;
      };

      $scope.pageChanged = function() {
        $scope.showSpinner = true;
        dataService.getRecords($scope.language, $scope.itemsPerPage, $scope.currentPage, $scope.text).then(recordsChanged);
        $window.scrollTo(0, 0);
        $timeout(function () {
          $scope.$apply();
        });
      };


      $scope.singleResult = function(apiId) {
        $scope.text = null;
        $scope.error = null;
        dataService.getRecord(apiId).then(function (result) {
          var record = result.data;
          record.showDetails = true;
          $scope.records = [record];
          // null so pagination section isn't shown
          $scope.totalItems = null;
          $location.search('id', result.data['api_id']);
          $timeout(function () {
            $scope.$apply();
          });
        }, function errorCallback(response) {
            $scope.error = "An error occurred, please try again. If the issue persist, please let us know.";
        });
      };

      $scope.enterSearch = function() {
        $scope.showSpinner = true;
        $scope.currentPage = undefined;
        $scope.error = null;
        $location.search('id', null);
        dataService.getRecords($scope.language, $scope.itemsPerPage, $scope.currentPage, $scope.text).then(recordsChanged);
      };

      $scope.expand = function (index) {
        $scope.records[index.$index].showDetails = !$scope.records[index.$index].showDetails;
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
