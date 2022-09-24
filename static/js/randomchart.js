// var getlabel = JSON.parse(document.getElementById("myChart2").dataset.getlabel);
// var getvalue = JSON.parse(document.getElementById("myChart2").dataset.getvalue);
var today = new Date();
var time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();

var studentname = [];
var studentage = [0]

var chartData = {
    labels : [],
    datasets : [{
        label: 'Data 1',
        fill: true,
        lineTension: 0.1,
        backgroundColor: 
            'rgba(255, 99, 132)',
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
        data : [0],
        spanGaps: false
    }]
    };
     
// get chart canvas
var ctx = document.getElementById("myChart2").getContext("2d");
    
// create the chart using the chart canvas
var myChart = new Chart(ctx, {
type: 'line',
data: chartData,
});

async function studentChart(){
    await getstudent()

}

async function getstudent(){
    const apiUrl = "https://demotest-flask-heroku.herokuapp.com/student"
    const response = await fetch(apiUrl);
    const alldata = await response.json();

    // console.log(alldata)
    studentname = alldata.map((x) => x.fname);
    studentage = alldata.map((x) => x.age);
    // const age = alldata.map((x) => x.age);
    console.log(studentname,studentage);
    myChart.data.labels = studentname;
    myChart.data.datasets[0].data = studentage;
    myChart.update();
}


fetch('https://reqres.in/api/users/5')
.then((response) =>{
    return response.json();
})
.then((json) =>{
    const user = json.data;
    const x1 = user.first_name + ' ' + user.last_name;
    const images = user.avatar;
    console.log(x1);
})
.catch((error) => {
    console.log(error.message);
});




function randomdata()
{
    var today = new Date();
    var time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
    var listdata = myChart.data.datasets[0].data;
    // console.log(listdata.length)
    if (listdata.length == 10){
        listdata.shift();
        myChart.data.labels.shift();
        listdata.push(Math.random(1,5));
        myChart.data.labels.push(time);
    }
    else{
        listdata.push(Math.random(1,5));
        myChart.data.labels.push(time);
    }
    
    myChart.update();
    console.log('update finish');
}


    //set time interval update
// setInterval(randomdata,1000);
setInterval(getstudent,10000);