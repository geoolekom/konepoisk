$(document).ready(function() {
    function loadUserChart () {
        var user_id = $('.user-info').data('user-id');
        $.get('/core/marks/?id=' + user_id, function(data) {
                var myChart = Highcharts.chart('user-chart', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Статистика оценок'
                },
                xAxis: {
                    categories: data['movies']
                },
                yAxis: {
                    title: {
                        text: null,
                    },
                    max: 10
                },
                series: [{
                    name: 'Оценки',
                    data: data['marks']
                }],
                legend: [{
                    enabled: false,
                }],
            });
        });

    };

    loadUserChart();

})