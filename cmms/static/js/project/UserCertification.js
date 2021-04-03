$(function () {

  var loadUserCertificationForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-userCertification").modal("show");
      },
      success: function (data) {
        $("#modal-userCertification .modal-content").html(data.html_userCertification_form);
        $('#id_userCertificationEnd').pDatepicker({
                                format: 'YYYY/MM/DD',

              autoClose: true,
              onSelect:function(unix){
                assetOfflineFrom=new Date(unix);
              }
            });
        $('#id_userCertificationStart').pDatepicker({
                                    format: 'YYYY/MM/DD',

                  autoClose: true,
                  onSelect: function(unix){

                   // var date1 = new Date(Date.parse($("#id_assetOfflineFrom").attr("value")));
                    // var date2 = new Date(Date.parse($("#id_assetOnlineFrom").attr("value")));
                    assetLifeOnlineFrom=new Date(unix);
                    // var timeDiff = Math.abs(assetLifeOnlineFrom.getTime() - assetLifeOfflineFrom.getTime());
                    // var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                    // alert(diffDays);
                  }
                                              });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveUserCertificationForm= function () {

   var form = $(this).parent();
   $.ajax({
     async: true,
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_userCertification").empty();
         $("#tbody_userCertification").html(data.html_userCertification_list);
         $("#modal-userCertification").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#userCertification-table tbody").html(data.html_userCertification_list);
         $("#modal-userCertification .modal-content").html(data.html_userCertification_form);
       }
     }
   });
   return false;
 };


 var deleteuserCert= function (event) {

   if(event.target.className=="btn btn-danger")
   {

    var form = $(this);


    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_userCertification").empty();
          $("#tbody_userCertification").html(data.html_userCertification_list);
          $("#modal-userCertification").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#userCertification-table tbody").html(data.html_userCertification_list);
          $("#modal-userCertification .modal-content").html(data.html_userCertification_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-userCertification").click(loadUserCertificationForm);

$("#userCertification-table").on("click", ".js-update-userCertification", loadUserCertificationForm);

$("#modal-userCertification").on("submit", ".js-userCertification-update-form", loadUserCertificationForm);
// Delete book
$("#userCertification-table").on("click", ".js-delete-userCertification", loadUserCertificationForm);
$("#modal-userCertification").on("click", ".js-userCertification-delete-form", deleteuserCert);

});
