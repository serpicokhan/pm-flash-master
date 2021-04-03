// var glll;
var drawIstgahStatusBar=function(data,dcolor,assetname)
{
  // console.log(data);

  mydataset=[]
  var Color=["#4dc9f6","#f67019","#f53794","#537bc4","blue","red","orange"]
  k=0;
  for( i in data){
    mydataset.push(
      {
        label: i,
        backgroundColor: dcolor[i+'-1'],
        borderColor: dcolor[i+'-1'],
        borderWidth: 1,
        data: data[i]
      }
    );

  }

  // console.log(data);
  var barData = {
    labels: assetname,
    datasets: mydataset,
  };
  console.log(barData);

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
var LoadIstgahStatusBar=function()
{

 // drawIstgahStatusBar();
}
