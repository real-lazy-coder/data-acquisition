// angular entry point
//http://angular-js.in/angular-busy/
var app = angular.module('DataLogger', ['ui.router', 'ngAnimate', 'cgBusy', 'toggle-switch']);

// change the symbol syntax as to not conflict with jinja templates.
app.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider) {
    // change angular syntax start and end points
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // url main
    $urlRouterProvider.otherwise('/home');

    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: '../static/partials/home.html'
        })
        .state('settings', {
            url: '/settings',
            templateUrl: '../static/partials/settings.html'
        })
});