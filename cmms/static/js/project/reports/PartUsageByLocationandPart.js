var randomScalingFactor = function() {
return Math.round(Math.random() * 100);
};

var randomData = function () {
return [
75,90,100
];
};

var randomValue = function (data) {
return Math.max.apply(null, data) * Math.random();
};

var data = randomData();





window.onload = function() {
  console.log(causedata);

drawCauseBar(causedata,"chart","گزارش روند مصرف قطعه");

};


// document.getElementById('randomizeData').addEventListener('click', function() {
// config.data.datasets.forEach(function(dataset) {
//  dataset.data = randomData();
//  dataset.value = randomValue(dataset.data);
// });

// window.myGauge.update();
//
//
//
// console.log(causedata);
// });
// var glll;
var drawCauseBar=function(data,element,lbl)
{
label=[];
dtset=[];
for(i in data)
{

  // console.log(i,data[i])
  label.push(i);
  dtset.push(data[i]);
}
  // console.log(data);
var barData = {
      labels: label,
      datasets: [
          {
              label:lbl,

              backgroundColor:"#F3F3F4",
              // borderColor:"#F3F3F4",

              data: dtset,
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


  var ctx3 = document.getElementById(element).getContext("2d");
  var myBarChart = new Chart(ctx3, {
    type: 'line',
    data: barData,
    options: barOptions
});
}
var drawCauseBar2=function(data,element,lbl)
{
label=[];
dtset=[];
for(i in data)
{

  // console.log(i,data[i])
  label.push(i);
  dtset.push(data[i]);
}
  // console.log(data);
var barData = {
      labels: label,
      datasets: [
          {
              label:lbl,

              backgroundColor:"#F3F3F4",
              // borderColor:"#F3F3F4",

              data: dtset,
               backgroundColor:["rgba(255, 99, 132, 0.2)","rgba(255, 159, 64, 0.2)","rgba(255, 205, 86, 0.2)","rgba(75, 192, 192, 0.2)","rgba(54, 162, 235, 0.2)","rgba(153, 102, 255, 0.2)","rgba(201, 203, 207, 0.2)"],"borderColor":["rgb(255, 99, 132)","rgb(255, 159, 64)","rgb(255, 205, 86)","rgb(75, 192, 192)","rgb(54, 162, 235)","rgb(153, 102, 255)","rgb(201, 203, 207)"]
          }
      ]
  };

  var barOptions = {
    title: {
       display: true,
       text:lbl
     }

  }


  var ctx3 = document.getElementById(element).getContext("2d");
  var myBarChart = new Chart(ctx3, {
    type: 'pie',
    data: barData,
    options: barOptions
});
}
