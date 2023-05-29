// var glll;
var drawTolidBar=function(data,label)
{




  // var barOptions = {
  //
  //   responsive: true,
  //   scales: {
  //
  //       yAxes: [{
  //           ticks: {
  //               beginAtZero: true,
  //               padding: 20
  //
  //           }
  //       }],
  //       y: {
  //      title: {
  //        display: true,
  //        text: 'Value'
  //      },
  //      min: 0,
  //      max: 100,
  //      ticks: {
  //        // forces step size to be 50 units
  //        stepSize: 50
  //      }
  //    }
  //   }
  // }
  // const data222 = {
  //   labels: label,
  //   datasets: [{
  //     axis: 'y',
  //     label: 'کیلومتر کارکرد',
  //     data: data,
  //     fill: true,
  //     backgroundColor: 'rgba(0, 128, 0, 0.5)' ,
  //     borderColor:'rgba(0, 128, 0, 1)',
  //     borderWidth: 5
  //   }]
  // };


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
console.log("$$$$$$$$$");
console.log(uniqueArray);
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

console.log("in");
console.log(data);

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

  $('#linetolidtime').remove(); // this is my <canvas> element
  $('#tolidtimelineholder').append('<canvas id="linetolidtime" height="100px"><canvas>');
  var ctx = document.getElementById("linetolidtime").getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: uniqueArray,
    datasets: datasets
  },
    options:  {
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

var LoadTolidBar=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: ''+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTolid/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      console.log(data);
      drawTolidBar(data.html_dashMTTR_list.s3,data.html_dashMTTR_list.s2);
      //html_DashMTTRCount_list






      // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

    },
    error:function(){
      alert("error");
    }
  });

}
var LoadTolidTimeBar=function()
{
  var location=$("#makans").val();
  $.ajax({
    url: ''+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTolidTime/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      if(location=='6961'){
        console.log("dsadsa");
      s1=data.html_dashMTTR_list.s3;
      console.log(s1);
      var dividedArray = s1.map(function(item) {
        var tmp=item*100;
        tmp= Math.floor(tmp / 180);
        var x1=Math.floor(tmp/3);
        return parseFloat(tmp.toString()+'.'+x1.toString())
      });
      drawTolidTimeBar(dividedArray,data.html_dashMTTR_list.s2);
    }
    else{

      drawTolidTimeBar(data.html_dashMTTR_list.s3,data.html_dashMTTR_list.s2);
    }
      //html_DashMTTRCount_list






      // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

    },
    error:function(){
      alert("error");
    }
  });

}
