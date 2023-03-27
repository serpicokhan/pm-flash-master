// var glll;
var drawEqDownTimeBar=function(data)
{

  console.log(data);
var barData = {
      labels: data.html_dashEqDownTime_list.dt2,
      datasets: [
          {
              label: "",
              fillColor: "rgba(220,220,220,0.5)",
              strokeColor: "rgba(220,220,220,0.8)",
              highlightFill: "rgba(220,220,220,0.75)",
              highlightStroke: "rgba(220,220,220,1)",
              data: data.html_dashEqDownTime_list.dt1,
              // backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(255, 159, 64, 0.2)","rgba(255, 205, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(54, 162, 235, 0.2)","rgba(153, 102, 255, 0.2)","rgba(201, 203, 207, 0.2)"],"borderColor":["rgb(255, 99, 132)","rgb(255, 159, 64)","rgb(255, 205, 86)","rgb(75, 192, 192)","rgb(54, 162, 235)","rgb(153, 102, 255)","rgb(201, 203, 207)"]
          }
      ]
  };

  var barOptions = {
      scaleBeginAtZero: true,
      scaleShowGridLines: true,
      scaleGridLineColor: "rgba(0,0,0,.05)",
      scaleGridLineWidth: 1,
      barShowStroke: true,
      barStrokeWidth: 2,
      barValueSpacing: 5,
      barDatasetSpacing: 1,
      responsive: true,
      scales: {
        yAxes: [{
            barPercentage: 0.1,
            gridLines: {
          display: false
        },
        }]
    },
    scales: {
      xAxes: [{
          barPercentage: 0.05,
          
      ticks: {
        beginAtZero: true
      }
      }]
  },

    legend: {
        "display": false
      },
  }


  var ctx = document.getElementById("barChart").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: barData,
    options: barOptions
});
}

var LoadEqDownTime=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetDownTime/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {

      drawEqDownTimeBar(data);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}
