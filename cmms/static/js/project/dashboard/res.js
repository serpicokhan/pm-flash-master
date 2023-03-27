var LoadResources=function()
{
  var location=$("#makans").val();

  $.ajax({
    url: 'Dashboard/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetResources/?loc='+location,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {



  $("#dash_restbody").html(data.html_dashAllResource_list);
  }
});
}
