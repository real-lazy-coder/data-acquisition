/**
 * Created by brent on 3/3/2015.
 */


$(function () {
    /**
     * Load new data depending on the selected min and max
     */
    function afterSetExtremes(e) {

        var chart = $('#container').highcharts();

        chart.showLoading('Loading data from server...');
        $.getJSON('api/history/search?min=' + Math.round(e.min) +
        '&max=' + Math.round(e.max), function (data) {

            chart.series[0].setData(data.log_data);
            chart.hideLoading();
        });
    }

    // See source code from the JSONP handler at https://github.com/highslide-software/highcharts.com/blob/master/samples/data/from-sql.php
    $.getJSON('api/history', function (data) {

        // Add a null value for the end date
        //data = [].concat(data.log_data, [[Date.now(), null, null, null, null]]);
        data = data.log_data;

        // create the chart
        $('#container').highcharts('StockChart', {
            chart: {
                type: 'spline',
                zoomType: 'x'
            },

            navigator: {
                adaptToUpdatedData: false,
                series: {
                    data: data
                }
            },

            scrollbar: {
                liveRedraw: false
            },

            title: {
                text: 'Freezer Temperature History'
            },

            subtitle: {
                text: 'Displaying 1.7 million data points in Highcharts Stock by async server loading'
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
                data: data,
                dataGrouping: {
                    enabled: false
                }
            }]
        });
    });
});
