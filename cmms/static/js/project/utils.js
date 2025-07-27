$(function () {
  var loadMails=function(url){
    
    $.ajax({

      url: url,



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
          console.log(data);
          

          //alert("response");
          //alert(data.html_assetPart_list);  // <-- This is just a placeholder for now for testing
          $("#statusMail").empty();
          $("#statusMail").html(data.html_mail_list);

          //console.log(data.html_wo_list);


      }
    });
 return false;


};
loadMails('/notification/list');


})
