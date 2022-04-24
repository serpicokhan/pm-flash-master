function DrawPMLineAll(data1,label,data2,label2)
{
  console.log("data",data1);
  // console.log("data",label);
  const data222 = {
  labels: label,
  datasets: [{
    axis: 'y',
    label: 'واکنشی',
    data: data1,
    fill: false,
    borderColor: 'red',
    borderWidth: 10
  },
  {
    axis: 'y',
    label: 'برنامه ریزی شده',
    data: data2,
    fill: false,
    borderColor: 'blue',
    borderWidth: 10
  }]
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

  $('#linepm').remove(); // this is my <canvas> element
  $('#pmlineholder').append('<canvas id="linepm"><canvas>');
  // console.log(element);
  // var ctx = document.getElementById("linepm");
  var ctx = document.getElementById("linepm").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'line',
    data: data222,

});



}
var dmoein=0;
function GetPmpLineAll(){
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetReactivevsRepatable/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);
      // dmoein=data;

    DrawPMLineAll(data.data.tamir,data.data.ttime,data.data.service,data.data.ftime);




  }
});
}
