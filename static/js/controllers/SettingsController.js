app.controller('SettingsController', ['$scope', '$http', function ($scope, $http) {
    $scope.lcdSwitch = false;

    $scope.switchLcd = function(){
        var value = $scope.lcdSwitch ? 1 : 0
        var apiUrl = 'settings/lcdSwitch?value=' + value;

        $http.get(apiUrl)
            .success(function(result){
                message = result.message;
                $scope.lcdSwitch = Boolean(message.lcdOn);
                var error = Boolean(message.error);
                if(error){
                    toastr.error(message.error);
                }else {
                    toastr.info(result.message.content);
                }
            })
            .error(function(){
                toastr.error('error switching LCD');
            });
    }
}]);