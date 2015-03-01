angular.module("myapp", [])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }])
    .controller("HelloController", function ($scope) {
        $scope.helloTo = {};
        $scope.helloTo.title = "Big Test";
    })
    .factory('TempHistory', function($resource){
        return $resource('/api/temperature')
    })