// var glll;
function generateUniqueRandomColors(count) {
    var colors = [];
    var colorSet = new Set(); // To keep track of generated colors

    while (colors.length < count) {
        var randomColor = '#' + Math.floor(Math.random() * 16777215).toString(16); // Generate a random hex color

        // Check if the color is unique (not already in the set)
        if (!colorSet.has(randomColor)) {
            colors.push(randomColor);
            colorSet.add(randomColor);
        }
    }

    return colors;
}
var drawTolidBar=function(data,label)
{




  // Extract labels and data
  const labels = [];
const datasets = [];

for (let datasetKey in data) {
  const datasetValues = data[datasetKey];

  const dataset = {
    label: datasetKey,
    data: [],
    borderColor: '#' + Math.floor(Math.random() * 16777215).toString(16), // Random color for line
    fill: false
  };

  for (let entry of datasetValues) {
    const [date, value] = Object.entries(entry)[0];
    // for(i in lables){
    //   if(i)
    // }
    // console.log(data);
    labels.push(date);
    dataset.data.push(value);
  }

  datasets.push(dataset);


}
const uniqueArray = Array.from(new Set(labels));
  $('#linetolid').remove(); // this is my <canvas> element
  $('#tolidlineholder').append('<canvas id="linetolid" height="100px"><canvas>');
  var ctx = document.getElementById("linetolid").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: uniqueArray,
    datasets: datasets
  },
    options: {
    responsive: true,
    legend: {
      display: true
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Labels'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Values'
        }
      }
    }
  }
  });

}
var drawTolidTimeBar=function(data,label)
{

console.log(data,label);

  const labels = [];
const datasets = [];

for (let datasetKey in data) {
  const datasetValues = data[datasetKey];

  const dataset = {
    label: datasetKey,
    data: [],

    // Random color for line
    fill: false
  };

  for (let entry of datasetValues) {
    const [date, value] = Object.entries(entry)[0];
    // for(i in lables){
    //   if(i)
    // }
    // console.log(data);
    labels.push(date);
    dataset.data.push(value);
  }

  datasets.push(dataset);


}
const uniqueArray = Array.from(new Set(labels));

  $('#linetolidtime').remove(); // this is my <canvas> element
  $('#tolidtimelineholder').append('<canvas id="linetolidtime" height="100px"><canvas>');
  var ctx = document.getElementById("linetolidtime").getContext("2d");
  const data2 = {
  labels:labels,
  datasets: [
    {
      label: 'Dataset 1',
      data: datasets,
    backgroundColor:generateUniqueRandomColors(labels.length),
    }
  ]
};
  const config = {
  type: 'doughnut',
  data: data2,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Doughnut Chart'
      }
    }
  },
};
console.log(uniqueArray);
console.log(datasets[0].data);
  // var myBarChart = new Chart(ctx, {
  //   type: 'doughnut',
  //   data: {
  //   labels: uniqueArray,
  //   datasets: datasets,
  //   backgroundColor:generateRandomColors(datasets.length),
  //
  // }, options: {
  //   responsive: true,
  //   plugins: {
  //     legend: {
  //       position: 'right',
  //     },
  //     title: {
  //       display: true,
  //       text: 'Chart.js Doughnut Chart'
  //     }
  //   }}
  //
  //
  // });
  new Chart(ctx, {
				type: 'doughnut',
				data: {
          labels:uniqueArray,

					// defaultFontFamily: 'Poppins',
					datasets: [{
						data: datasets[0].data,
            labels:uniqueArray,

						borderColor: "rgba(255,255,255,1)",
						backgroundColor: generateUniqueRandomColors(datasets[0].data.length),


					}],
					// labels: [
					//     "green",
					//     "green",
					//     "green",
					//     "green"
					// ]
				},
				options: {
					weight: 1,
					cutoutPercentage: 70,
          legend: {
                   position: 'right', // Position the legend on the right
               },

				}
			});
}

var LoadTolidBar=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: '/Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTolidMain?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);
      drawTolidBar(data.html_dashMTTR_list.s3,data.html_dashMTTR_list.s2);
      //html_DashMTTRCount_list






      // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

    },
    error:function(){
      alert("error");
    }
  });

}
var LoadTolidDonut=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: '/Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTolidDonut/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
    //   if(location=='6961'){
    //     console.log("dsadsa");
    //   s1=data.html_dashMTTR_list.s3;
    //   console.log(s1);
    //   var dividedArray = s1.map(function(item) {
    //     var tmp=item*100;
    //     tmp= Math.floor(tmp / 180);
    //     var x1=Math.floor(tmp/3);
    //     return parseFloat(tmp.toString()+'.'+x1.toString())
    //   });
    //   drawTolidTimeBar(dividedArray,data.html_dashMTTR_list.s2);
    // }
    // else{

      drawTolidTimeBar(data.html_dashMTTR_list.s3,data.html_dashMTTR_list.s2);
    // }
      //html_DashMTTRCount_list






      // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

    },
    error:function(){
      alert("error");
    }
  });

}
var LoadTolidBarChart=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: $("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTolidBar/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data2) {


      data=data2.html_dashMTTR_list.s3;
      // Formatting data for Chart.js
      const labels = Object.keys(data);
      const datasets = labels.map((label) => ({
          label: `برج ${label}`,
          data: data[label].map((item) => parseFloat(item.val)),
          backgroundColor: '#' + Math.floor(Math.random() * 16777215).toString(16), // Adjust as needed
          borderColor: '#' + Math.floor(Math.random() * 16777215).toString(16), // Adjust as needed
          borderWidth: 1
      }));
      console.log(datasets);

      // Creating the bar chart
      $('#bartolid').remove(); // this is my <canvas> element
      $('#tolidbarholder').append('<canvas id="bartolid" height="100px"><canvas>');
      // var ctx = document.getElementById("linetolidtime").getContext("2d");
      const ctx = document.getElementById('bartolid').getContext('2d');
      new Chart(ctx, {
          type: 'bar',
          data: {
              labels: labels,
              datasets: datasets
          },
          options: {
              scales: {
                yAxes: [{
           ticks: {
               beginAtZero: true
           }
       }]
              }
          }
      });
      // drawTolidTimeBar(data.html_dashMTTR_list.s3,data.html_dashMTTR_list.s2);


    },
    error:function(){
      alert("error");
    }
  });

}
