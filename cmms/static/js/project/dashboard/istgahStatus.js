// var glll;
var drawIstgahStatusBar=function(data,dcolor,assetname)
{
  // console.log(data);

  mydataset=[]
  var Color=[ 'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'];
      borderColor= [
         'rgb(255, 99, 132)',
         'rgb(255, 159, 64)',
         'rgb(255, 205, 86)',
         'rgb(75, 192, 192)',
         'rgb(54, 162, 235)',
         'rgb(153, 102, 255)',
         'rgb(201, 203, 207)'
       ];
  k=0;
  for( i in data){
    mydataset.push(
      {
        label: i,
        backgroundColor: Color[k],
        borderColor: borderColor[k],
        borderWidth:0.5,
        data: data[i]
      }
    );
    k++;

  }

  // console.log(data);
  var barData = {
    labels: assetname,
    datasets: mydataset,
  };
  // console.log(barData);

  var chartOptions = {
    responsive: true,
    legend: {
      position: "top"
    },
    title: {
      display: true,
      text: "وضعیت ایستگاهها به ساعت"
    },
    scales: {
      yAxes: [{
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


  }

  $('#istgahBarChart').remove(); // this is my <canvas> element
  $('#graph-container').append('<canvas id="istgahBarChart" height="100px"><canvas>');

  var ctx = document.getElementById("istgahBarChart").getContext("2d");

  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: barData,
    options: chartOptions
});
}
var LoadEqCost=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetIstgahStatus/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);

    drawIstgahStatusBar(data.html_DashIstgahStatus_list.dt1,data.html_DashIstgahStatus_list.dt2,data.html_DashIstgahStatus_list.dt3);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}
var LoadEqCost2=function(loc)
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetIstgahStatus2/'+loc,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);

    drawIstgahStatusBar(data.html_DashIstgahStatus_list.dt1,data.html_DashIstgahStatus_list.dt2,data.html_DashIstgahStatus_list.dt3);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}
$(".darayeeselector").click(function(){
loc=($(this).attr("date-url"));
LoadEqCost2(loc);
return false;
});
var LoadIstgahStatusBar=function()
{

 // drawIstgahStatusBar();
}
