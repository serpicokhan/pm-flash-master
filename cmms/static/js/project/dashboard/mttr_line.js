// var glll;
var drawMTTRBar=function(data,label)
{


  // console.log(data);
var barData = {
      labels: label,
      datasets: [
          {
              label: "mttr",

              backgroundColor:"#F3F3F4",
              // borderColor:"#F3F3F4",

              data: data,
               backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(255, 159, 64, 0.2)","rgba(255, 205, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(54, 162, 235, 0.2)","rgba(153, 102, 255, 0.2)","rgba(201, 203, 207, 0.2)"],"borderColor":["rgb(255, 99, 132)","rgb(255, 159, 64)","rgb(255, 205, 86)","rgb(75, 192, 192)","rgb(54, 162, 235)","rgb(153, 102, 255)","rgb(201, 203, 207)"]
          }
      ]
  };

  var barOptions = {
      scaleBeginAtZero: true,
      scaleShowGridLines: true,
      scaleGridLineColor: "#F3F3F4",
      scaleGridLineWidth: 1,
      barShowStroke: true,
      barStrokeWidth: 2,
      barValueSpacing: 5,
      barDatasetSpacing: 1,
      responsive: true,
      scaleFontColor: "#FFFFFF",
      scales: {
        xAxes: [{
            barPercentage: 0.15,
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
  const data222 = {
  labels: label,
  datasets: [{
    axis: 'y',
    label: 'متوسط زمان تعمیر',
    data: data,
    fill: false,
    backgroundColor: 'rgba(54, 162, 235, 0.2)' ,
  borderColor:'rgb(54, 162, 235)',
    borderWidth: 10
  }]
};

  $('#mttr_line_chart').remove(); // this is my <canvas> element
  $('#MTTRgraph-container').append('<canvas id="mttr_line_chart" height="100px"><canvas>');
  var ctx = document.getElementById("mttr_line_chart").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'line',
    data: data222,
    options: barOptions
});
}

var LoadMTTRBar=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetMTTR/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      console.log(data);
      drawMTTRBar(data.html_dashMTTR_list.s1,data.html_dashMTTR_list.s2);
      //html_DashMTTRCount_list






  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

},
error:function(){
  alert("error");
}
});

}
var LoadMTTRBar2=function(loc)
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetMTTRCount2/'+loc,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);
      drawMTTRBar(data.html_DashMTTRCount_list.dt1);
      //html_DashMTTRCount_list






  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

},
error:function(){
  alert("error");
}
});

}
