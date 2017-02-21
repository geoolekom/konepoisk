$(document).ready(function() {
    function loadUserChart () {
        var user_id = $('.user-info').data('user-id');
        $.get('/api/users/' + user_id + '.json', function(data) {
        		var set = data['moviemark_set'];
        		var movies = Array();
        		var marks = Array();
        		for (i = 0; i < set.length; i++) {
        			movies.push(set[i]['movie']['title']);
        			marks.push(set[i]['value'])
                }
                var myChart = Highcharts.chart('user-chart', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Статистика оценок'
                },
                xAxis: {
                    categories: movies
                },
                yAxis: {
                    title: {
                        text: null,
                    },
                    max: 10
                },
                series: [{
                    name: 'Оценка',
                    data: marks
                }],
                legend: [{
                    enabled: false,
                }],
            });
        });

    };

    loadUserChart();

})