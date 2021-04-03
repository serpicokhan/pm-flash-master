function DrawDonat(data1,data2,element)
{
  var doughnutData =
  {
        labels: ["تکمیل به موقع", "کامل شده"],
        datasets: [
          {
            label: "",
            backgroundColor: ["#c2c2c2", "#1ab394"],
            data: [data1-data2,data2]
          }
        ]
      };


  // [
  //     {
  //         value: data1-data2,
  //         color: "#49C6F4",
  //         highlight: "#CEEEFD",
  //         label: "Completed On Time"
  //     },
  //     {
  //         value: data2,
  //         color: "#01A9F4",
  //         highlight: "#1ab394",
  //         label:""
  //     }
  //
  // ];

  var doughnutOptions = {
      // segmentShowStroke: true,
      // segmentStrokeColor: "#fff",
      // segmentStrokeWidth: 2,
      // percentageInnerCutout: 45, // This is 0 for Pie charts
      // animationSteps: 100,
      // animationEasing: "easeOutBounce",
      // animateRotate: true,
      // animateScale: false,
      // responsive: true,
      // borderWidth:10
      title: {
        display: false,
        text: ''
      },
      legend: {
        display: false,
        //position: 'right'
    },

  };


  var ctx = document.getElementById(element).getContext("2d");
  //var myNewChart = new Chart(ctx).Doughnut(doughnutData, doughnutOptions);
   if(data1 === 0 && data2==0)
   {
    $("#"+element).parent().children("h3").show();
      $("#"+element).hide();

   }
  else {
    $("#"+element).parent().children("h3").hide();
      $("#"+element).show();
    var myNewChart = new Chart(ctx, {
      type: 'doughnut',
      data: doughnutData,
      options: doughnutOptions
  });

  }

}

//*****************************show categorized completed workorder*******************

function DrawDonat2(data,element)
{

  var doughnutData =
  {

        labels: data.woCompletedAssetId,
        datasets: [
          {
            label: "Population (millions)",
            backgroundColor: ["#c2c2c2", "#1ab394","#f8ac59"],
            data:data.woCompletedNum
          }
        ]
      };


  // [
  //     {
  //         value: data1-data2,
  //         color: "#49C6F4",
  //         highlight: "#CEEEFD",
  //         label: "Completed On Time"
  //     },
  //     {
  //         value: data2,
  //         color: "#01A9F4",
  //         highlight: "#1ab394",
  //         label:""
  //     }
  //
  // ];

  var doughnutOptions = {
      // segmentShowStroke: true,
      // segmentStrokeColor: "#fff",
      // segmentStrokeWidth: 2,
      // percentageInnerCutout: 45, // This is 0 for Pie charts
      // animationSteps: 100,
      // animationEasing: "easeOutBounce",
      // animateRotate: true,
      // animateScale: false,
      // responsive: true,
      // borderWidth:10
      title: {
        display: true,
        text: ''
      },
      legend: {
        display: true,
        position: 'right'
    },

  };


  var ctx = document.getElementById(element).getContext("2d");
  console.log("shoru");
  console.log(data.woCompletedNum.length);
  console.log("tamam");
  if(data.woCompletedNum.length==1)
  {
   $("#"+element).parent().children("h3").show();
    $("#"+element).hide();

  }
  else {
    $("#"+element).parent().children("h3").hide();
    $("#"+element).show();
    var myNewChart = new Chart(ctx, {
      type: 'doughnut',
      data: doughnutData,
      options: doughnutOptions
  });
  }
  //var myNewChart = new Chart(ctx).Doughnut(doughnutData, doughnutOptions);

}
var LoadCompletedWorkOrderDonat=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetCompletedWoDonat/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      console.log(data);

    DrawDonat2(data.html_dashWoStatusDonat_list,'woCompletedDoughnutChart');
    // $('#onDemWoComOnTimedh4').text(data.html_dashwoCompleted_list.woCompletedOnTimeNum);
    // $('#onDemWoComh4').text(data.html_dashwoCompleted_list.woCompletedNum);
  }
});
}
//******************************
var LoadOnDemandDonat=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/'+0+'/GetCompletedWo/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {

    DrawDonat(data.html_dashwoCompleted_list.woCompletedNum,data.html_dashwoCompleted_list.woCompletedOnTimeNum,'doughnutChartOnDemand');
    $('#onDemWoComOnTimedh4').text(data.html_dashwoCompleted_list.woCompletedOnTimeNum);
    $('#onDemWoComh4').text(data.html_dashwoCompleted_list.woCompletedNum);
  }
});
}
var LoadPmDonat=function()
{
  $.ajax({
  url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/'+1+'/GetCompletedWo/',
  type: 'get',
  dataType: 'json',
  beforeSend: function () {

  },
  success: function (data) {

  DrawDonat(data.html_dashwoCompleted_list.woCompletedNum,data.html_dashwoCompleted_list.woCompletedOnTimeNum,'doughnutChartpm');
  $('#pmWoComOnTimedh4').text(data.html_dashwoCompleted_list.woCompletedOnTimeNum);
  $('#pmWoComh4').text(data.html_dashwoCompleted_list.woCompletedNum);
}
});
}
var LoadTotalDonat=function()
{
  $.ajax({
  //url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetTotalCompletedWo/',dash_GetAllWorkOrders
  url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetAllWorkOrders/',
  type: 'get',
  dataType: 'json',
  beforeSend: function () {

  },
  success: function (data) {

  DrawDonat(data.html_dashAllWorkOrders_list.TotalwoCompletedNum,data.html_dashAllWorkOrders_list.TotalOnTimeCompletedWorkOrderNum,'doughnutChartTotal');
  $('#totalWoComOnTimedh4').text(data.html_dashAllWorkOrders_list.GetAvgDaysToCompletedNum);
  $('#totalWoComh4').text(data.html_dashAllWorkOrders_list.GetAvgTotalCostPerWO);
  }
  });
}
