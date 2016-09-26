'use strict';

/**
 * @ngdoc overview
 * @name g4seApp
 * @description
 * # g4seApp
 *
 * Main module of the application.
 */
angular
  .module('g4seApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.bootstrap',
    'angularSpinner'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/search.html',
        controller: 'SearchCtrl',
        controllerAs: 'search',
        reloadOnSearch: false
      }).otherwise({
        redirectTo: '/'
      });
  });
