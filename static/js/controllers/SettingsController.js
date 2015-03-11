app.controller('SettingsController', ['$scope', '$http', function ($scope, $http) {
    $scope.lcdSwitch = false;

    $scope.switchLcd = function(){
        var value = $scope.lcdSwitch ? 1 : 0
        var apiUrl = 'settings/lcdSwitch?value=' + value;

        $http.get(apiUrl)
            .success(function(result){
                toastr.info(result.message);
            })
            .error(function(){
                toastr.error('error switching LCD');
            });
    }
}]);