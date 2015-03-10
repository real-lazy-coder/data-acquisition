app.controller("HistoryCtrl", ['$scope', 'dataFactory', function ($scope, dataFactory) {

    function getHistory() {
        dataFactory.getHistory()
            .success(function (hist) {
                $scope.history = hist.log_data;
            })
            .error(function (error) {
                $scope.status = 'Unable to load history: ' + error.message;
            })
    }



}]);

app.factory('dataFactory', ['$http', function ($http) {
    var urlBase = '/api/history';
    var dataFactory = {};

    dataFactory.getHistory = function () {
        return $http.get(urlBase);
    };

    return dataFactory;
}]);