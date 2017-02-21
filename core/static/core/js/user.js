$(document).ready(function() {
    function loadUserChart () {
        var user_id = $('.user-info').data('user-id');
        $.get('/core/marks/?id=' + user_id, function(data) {
                var myChart = Highcharts.chart('user-chart', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Оценки фильма'
                },
                xAxis: {
                    categories: data['movies']
                },
                yAxis: {
                    title: {
                        text: 'Пользователи'
                    }
                },
                series: [{
                    name: 'Оценки',
                    data: data['marks']
                }],
            });
        });

    };

    loadUserChart();

})