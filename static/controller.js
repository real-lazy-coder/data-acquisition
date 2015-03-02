var app = angular.module('DataLogger', []);

app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller("HistoryCtrl", function ($scope, $http) {
    $scope.config = {
        title: 'Products',
        tooltips: true,
        labels: false,
        mouseover: function () {
        },
        mouseout: function () {
        },
        click: function () {
        },
        legend: {
            display: true,
            //could be 'left, right'
            position: 'right'
        }
    };

    $http.get('/api/history')
        .then(function (res) {
            $scope.data = res.data.log_data;
        });
});