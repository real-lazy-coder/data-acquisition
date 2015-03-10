// angular entry point
var app = angular.module('DataLogger', ['ui.router', 'highcharts-ng']);

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
        });
});