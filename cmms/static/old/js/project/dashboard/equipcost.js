// var glll;
var drawEqCostBar=function(data)
{

  console.log(data);
var barData = {
      labels: data.html_dashEqCost_list.dt1,
      datasets: [
          {
              label: "هزینه تجهیزات به میلیون",
              fillColor: "rgba(220,220,220,0.5)",
              strokeColor: "rgba(220,220,220,0.8)",
              highlightFill: "rgba(220,220,220,0.75)",
              highlightStroke: "rgba(220,220,220,1)",
              data: data.html_dashEqCost_list.dt2,
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
      scaleFontColor: "#FFFFFF",
      scales: {
        xAxes: [{
            barPercentage: 0.05,
            gridLines: {
          display: false
        },
        ticks: {
          beginAtZero: true
        }
        }]
    },



    "animation": {
      "duration": 1,
      "onComplete": function() {
        var chartInstance = this.chart,
          ctx = chartInstance.ctx;

        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);

        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';

        this.data.datasets.forEach(function(dataset, i) {
          var meta = chartInstance.controller.getDatasetMeta(i);
          meta.data.forEach(function(bar, index) {
            var data = dataset.data[index];
            ctx.fillText(data, bar._model.x, bar._model.y - 5);
          });
        });
      }
    },
    legend: {
      "display": true
    },

  }


  var ctx = document.getElementById("eqcostbarChart").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: barData,
    options: barOptions
});
}

var LoadEqCost=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetEquipCost/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {

      drawEqCostBar(data);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}
