var LoadResources=function()
{
  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetResources/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      

  $("#dash_restbody").html(data.html_dashAllResource_list);
  }
});
}
