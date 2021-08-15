function DrawResourceStatusDonat(element,gid,date1,date2)
{
  var doughnutData =
  {
        labels: ["ساعت حضور","ساعت کارکرد"],
        datasets: [
          {
            label: "",
            backgroundColor: ["#c2c2c2", "#1ab394"],
            data: [date2, date1]
          }
        ]
      };



  var doughnutOptions = {
      title: {
        display: false,
        text: ''
      },
      legend: {
        display: false,
        position: 'right'
    },

  };
console.log("gid",gid);
  $('.doughnutChartResourceStatus'+gid).remove(); // this is my <canvas> element
  $('#dchartcontainer'+gid).append('<canvas class="doughnutChartResourceStatus'+gid+'" style="width: 78px; height: 78px;"><canvas>');
  console.log(element);
  var ctx = document.getElementsByClassName(element)[0].getContext("2d");

    var myNewChart = new Chart(ctx, {
      type: 'doughnut',
      data: doughnutData,
      options: doughnutOptions
  });



}
function DrawResourceStatusDonat2(element,data,gid)
{
  label=[];
  dtset=[];
  col=[];
  for( i in data)
  {
    if(i[0]!='c'){
    label.push(i);
    dtset.push(data[i]);
  }
  else{
    col.push(data[i]);
  }
  }
  var doughnutData =
  {
        labels: label,
        datasets: [
          {
            label: "",
            backgroundColor: col,
            data: dtset
          }
        ]
      };



  var doughnutOptions = {
      title: {
        display: false,
        text: ''
      },
      legend: {
        display: false,
        position: 'right'
    },

  };

  $('.pieChartResourceStatus'+gid).remove(); // this is my <canvas> element
  $('#pgidcontainer'+gid).append('<canvas class="pieChartResourceStatus'+gid+'" style="width: 78px; height: 78px;"><canvas>');

  var ctx = document.getElementsByClassName(element)[0].getContext("2d");

    var myNewChart = new Chart(ctx, {
      type: 'doughnut',
      data: doughnutData,
      options: doughnutOptions
  });



}

//*****************************show categorized completed workorder*******************
var LoadResource=function(gid,element)
{
  // console.log(a111);
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/'+gid+'/GetResStatus/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);

    DrawResourceStatusDonat("doughnutChartResourceStatus"+gid,gid,data.html_DashResourceStatus_list.dt1,data.html_DashResourceStatus_list.dt2);
    $(".pmWoComOnTimedh"+gid).text(data.html_DashResourceStatus_list.dt1)
    $(".pmWoComh"+gid).text(data.html_DashResourceStatus_list.dt2)
    DrawResourceStatusDonat2("pieChartResourceStatus"+gid,data.html_DashResourceStatus_list.dt3,gid);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}
var LoadResource2=function(gid,element,loc)
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/'+gid+'/GetResStatus2/'+loc,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      // console.log(data);

    DrawResourceStatusDonat("doughnutChartResourceStatus"+gid,gid,data.html_DashResourceStatus_list.dt1,data.html_DashResourceStatus_list.dt2);
    $(".pmWoComOnTimedh"+gid).text(data.html_DashResourceStatus_list.dt1)
    $(".pmWoComh"+gid).text(data.html_DashResourceStatus_list.dt2)
    DrawResourceStatusDonat2("pieChartResourceStatus"+gid,data.html_DashResourceStatus_list.dt3,gid);


  // $("#dash_eqdowntimebody").html(data.html_dashEqDownTime_list);

  }
});
}


//******************************
