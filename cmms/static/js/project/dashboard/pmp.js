function DrawPMPDonatAll(data1,data2)
{


  $('#donutpmp').remove(); // this is my <canvas> element
  $('#pmpholder').append('<canvas id="donutpmp"><canvas>');
  // console.log(element);
  var ctx = document.getElementById("donutpmp");

  var myChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['برنامه ریزی شده','واکنشی'],
    datasets: [{
      label: '# of Tomatoes',
      data: [data1,data2],
      backgroundColor: [
        'blue',
        'red',
        'rgba(75, 192, 192, 0.2)',

        'rgba(255, 206, 86, 0.2)',

      ],
      borderColor: [
        'rgba(54, 162, 235, 1)',
        'rgba(255,99,132,1)',
          'rgba(75, 192, 192, 1)',

        'rgba(255, 206, 86, 1)',

      ],
      borderWidth: 1
    }]
  },
  options: {
   	//cutoutPercentage: 40,
    responsive: false,
    cutoutPercentage: 70,
    plugins: {
           legend: true // Hide legend
       },

  }
});

}
function GetPmpAll(){
  var location=$("#makans").val();
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetPMPALL/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {

    DrawPMPDonatAll(data.pm,data.unpm);




  }
});
}
