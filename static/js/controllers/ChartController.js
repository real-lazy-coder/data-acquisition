app.controller("ChartController", ['$scope', 'chartHistoryFactory', function ($scope, chartHistoryFactory) {

    tempData = [];
    var chart;
    function getHistory() {
        chartHistoryFactory.getHistory()
            .success(function (hist) {
                tempData = hist.log_data;
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
                        selected: 5 // all
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
            })
            .error(function (error) {
                $scope.status = 'Unable to load history: ' + error.message;
            })
    }

    getHistory();

    function getLastPoint(chart) {
        var series = chart.series[0];
        setInterval(function () {
            $.getJSON('api/temp/last_log_point', function (data) {
                var x = data.point[0];
                var y = data.point[1];
                series.addPoint([x, y], true, true);
            });
        }, 60000);
    }

    function afterSetExtremes(e) {
        chart.showLoading('Loading data from server...');
        $.getJSON('api/temp/history/search?min=' + Math.round(e.min) + '&max=' + Math.round(e.max), function (data) {
            chart.series[0].setData(data.log_data);
            chart.hideLoading();

            getLastPoint(chart);
        });
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


    app.factory('chartHistoryFactory', ['$http', function ($http) {
        var urlBase = '/api/temp/history';
        var chartHistoryFactory = {};

        chartHistoryFactory.getHistory = function () {
            return $http.get(urlBase);
        };

        return chartHistoryFactory;
    }]);
