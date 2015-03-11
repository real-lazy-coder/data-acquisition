app.controller("ChartController", ['$scope', '$http', 'chartHistoryFactory', function ($scope, $http, chartHistoryFactory) {

    tempData = [];
    var chart;

    // used for angular-busy
    $scope.delay = 0;
    $scope.minDuration = 0;
    $scope.message = 'Loading Data From Server...';
    $scope.backdrop = true;
    $scope.promise = null;

    function getHistory() {
        // primise is used for angular-busy
        $scope.promise = $http.get('/api/temp/history')
            .success(function (hist) {
                tempData = hist.log_data;
                // highstocks.js chart setup
                chart = new Highcharts.StockChart({

                    chart: {
                        type: 'spline',
                        zoomType: 'x',
                        renderTo: 'chart1'
                    },
                    navigator: {
                        adaptToUpdatedData: false,
                        series: {
                            data: tempData
                        }
                    },

                    scrollbar: {
                        liveRedraw: false
                    },

                    title: {
                        text: 'Freezer Temperature History'
                    },

                    subtitle: {
                        text: ''
                    },

                    rangeSelector: {
                        buttons: [{
                            type: 'minute',
                            count: 30,
                            text: '30m'
                        }, {
                            type: 'hour',
                            count: 1,
                            text: '1h'
                        }, {
                            type: 'hour',
                            count: 6,
                            text: '6h'
                        }, {
                            type: 'day',
                            count: 1,
                            text: '1d'
                        }, {
                            type: 'all',
                            text: 'All'
                        }],
                        inputEnabled: false, // it supports only days
                        selected: 2 // this number represents an array starting with 0 through buttons.len
                    },

                    xAxis: {
                        events: {
                            afterSetExtremes: afterSetExtremes
                        },
                        minRange: 1800 * 1000 // 30 minutes
                    },

                    yAxis: {
                        floor: -40
                    },

                    series: [{
                        data: tempData,
                        dataGrouping: {
                            enabled: false
                        }
                    }]
                })
                //getLastPoint(chart)
            })
            .error(function (error) {
                $scope.status = 'Unable to load history: ' + error.message;
            })
    }

    getHistory();

    // retrieve the last point from the database
    function getLastPoint(chart) {
        var series = chart.series[0];
        var apiUrl = 'api/temp/last_log_point';
        setInterval(function () {
            $http.get(apiUrl)
                .success(function (data) {
                    var x = data.point[0];
                    var y = data.point[1];
                    series.addPoint([x, y], true, true);
                })
                .error(function (error) {
                    $scope.apiStatus = {
                        error: error.message
                    }
                })
        }, 60000);
    }

    // retrieve the data from the server after zoom
    function afterSetExtremes(e) {
        chart.showLoading('Loading data from server...');
        var apiUrl = 'api/temp/history/search?min=' + Math.round(e.min) + '&max=' + Math.round(e.max)
        $http.get(apiUrl)
            .success(function (data) {
                chart.series[0].setData(data.log_data);
                chart.hideLoading();
                //getLastPoint(chart);
            })
            .error(function (error) {
                $scope.apiStatus = {
                    error: error.message
                }
            })
    }

}]);
// create the chart
//$('#container').highcharts('StockChart', {
//    chart: {
//        type: 'spline',
//        zoomType: 'x'
//    },
//
//    navigator: {
//        adaptToUpdatedData: false,
//        series: {
//            data: tempData
//        }
//    },
//
//    scrollbar: {
//        liveRedraw: false
//    },
//
//    title: {
//        text: 'Freezer Temperature History'
//    },
//
//    subtitle: {
//        text: ''
//    },
//
//    rangeSelector: {
//        buttons: [{
//            type: 'minute',
//            count: 30,
//            text: '30m'
//        }, {
//            type: 'hour',
//            count: 1,
//            text: '1h'
//        }, {
//            type: 'hour',
//            count: 6,
//            text: '6h'
//        }, {
//            type: 'day',
//            count: 1,
//            text: '1d'
//        }, {
//            type: 'all',
//            text: 'All'
//        }],
//        inputEnabled: false, // it supports only days
//        selected: 5 // all
//    },
//
//    xAxis: {
//        events: {
//            afterSetExtremes: afterSetExtremes
//        },
//        minRange: 1800 * 1000 // 30 minutes
//    },
//
//    yAxis: {
//        floor: -40
//    },
//
//    series: [{
//        data: tempData,
//        dataGrouping: {
//            enabled: false
//        }
//    }]
//});

// factory to retrieve data from server
app.factory('chartHistoryFactory', ['$http', function ($http) {
    var urlBase = '/api/temp/history';
    var chartHistoryFactory = {};

    chartHistoryFactory.getHistory = function () {
        return $http.get(urlBase);
    };

    return chartHistoryFactory;
}]);
