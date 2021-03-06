var getlabel = JSON.parse(document.getElementById("myChart1").dataset.getlabel);
var getvalue = JSON.parse(document.getElementById("myChart1").dataset.getvalue);

var chartData = {
    labels : getlabel,
    datasets : [{
        // label: '{{ legend }}',
        fill: true,
        lineTension: 0.1,
        backgroundColor: 
            'rgba(255, 99, 132, 0.2)',
            // 'rgba(54, 162, 235, 0.2)',
            // 'rgba(255, 206, 86, 0.2)',
            // 'rgba(75, 192, 192, 0.2)',
            // 'rgba(153, 102, 255, 0.2)',
            // 'rgba(255, 159, 64, 0.2)'
        
        borderColor: 
            'rgba(255, 99, 132, 1)',
            // 'rgba(54, 162, 235, 1)',
            // 'rgba(255, 206, 86, 1)',
            // 'rgba(75, 192, 192, 1)',
            // 'rgba(153, 102, 255, 1)',
            // 'rgba(255, 159, 64, 1)'
        
        borderWidth: 1,
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: "rgba(75,192,192,1)",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(75,192,192,1)",
        pointHoverBorderColor: "rgba(220,220,220,1)",
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data : getvalue,
        spanGaps: false
    }]
    };
     
    // get chart canvas
    var ctx = document.getElementById("myChart1").getContext("2d");
     
    // create the chart using the chart canvas
    var myChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    });