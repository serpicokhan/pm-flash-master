function DrawWoGroupBar(data){
  console.log(data);

var wogroupbarbarChartData = {
  labels: [
    "درخواست سفارشی",
    "درخواست خودکار",

  ],
  datasets: [
    {
      label: "منقضی شده",
      backgroundColor: "pink",
      borderColor: "red",
      borderWidth: 1,
      data: [data.html_dashWoStatus_list.dash_WoStatus_w10, data.html_dashWoStatus_list.dash_PmStatus_p10]
    },
    {
      label: "متوقف",
      backgroundColor: "lightblue",
      borderColor: "blue",
      borderWidth: 1,
      data: [data.html_dashWoStatus_list.dash_WoStatus_w2, data.html_dashWoStatus_list.dash_PmStatus_p2]
    },
    {
      label: "منتظر قطعه",
      backgroundColor: "lightgreen",
      borderColor: "green",
      borderWidth: 1,
      data: [data.html_dashWoStatus_list.dash_WoStatus_w9, data.html_dashWoStatus_list.dash_PmStatus_p9]
    },
    {
      label: "در حال پیشرفت",
      backgroundColor: "yellow",
      borderColor: "orange",
      borderWidth: 1,
      data: [data.html_dashWoStatus_list.dash_WoStatus_w6, data.html_dashWoStatus_list.dash_PmStatus_p6]
    }
  ]
};

var wogroupbarchartOptions = {
  responsive: true,
  legend: {
    position: "top"
  },
  title: {
    display: true,
    text: "Chart.js Bar Chart"
  },
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true
      }
    }],
    xAxes: [{
           barPercentage: 0.4
       }]
  }
}
var ctx = document.getElementById("wogroupbarcanvas").getContext("2d");
var myBar = new Chart(ctx, {
  type: "bar",
  data: wogroupbarbarChartData,
  options: wogroupbarchartOptions
});
}

var LoadGroupBar=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetCompletedOpenStatus/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      console.log(data);

    DrawWoGroupBar(data);

  }
});
}
