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
    'ngCookies',
    'ngRoute'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .when('/', {
        templateUrl: 'views/search.html',
        controller: 'SearchCtrl',
        controllerAs: 'search'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
