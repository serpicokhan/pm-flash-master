$(function () {

  var loadOfflineStatusForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-offlineStatus").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-offlineStatus .modal-content").html(data.html_offlineStatus_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveOfflineStatusForm= function () {


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
         $("#tbody_offlineStatus").empty();
         $("#tbody_offlineStatus").html(data.html_offlineStatus_list);
         $("#modal-offlineStatus").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#offlineStatus-table tbody").html(data.html_offlineStatus_list);
         $("#modal-offlineStatus .modal-content").html(data.html_offlineStatus_form);
       }
     }
   });
   return false;
 };

   var deleteOfflineStatus=function(id){
     $.ajax({
       async: true,
       url: '/SettingPage/OfflineStatus/'+id+'/Delete/',

       type: 'get',
       dataType: 'json',
       success: function (data) {
         console.log(data);
         if (data.form_is_valid) {
           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           $("#tbody_offlineStatus").empty();
           $("#tbody_offlineStatus").html(data.html_offlineStatus_list);
           $("#modal-offlineStatus").modal("hide");
           //console.log(data.html_wo_list);
         }
         else {

           $("#offlineStatus-table tbody").html(data.html_offlineStatus_list);
           $("#modal-offlineStatus .modal-content").html(data.html_offlineStatus_form);
         }
       }
     });

     return false;
   }
   $('#offlineStatus-table').on('click','.js-delete-offlineStatus', function () {
   const dashassetid=($(this).attr('data-url'));

     swal({
       title: "??????",
       text: "??????",
       type: "warning",
       showCancelButton: true,
       confirmButtonColor: "#DD6B55",
       confirmButtonText: "??????",
       cancelButtonText: "??????",
       closeOnConfirm: true
      }, function () {
          // cancelform();
          deleteOfflineStatus(dashassetid);

      });

     // do something???
   });

 /////////////////////////////

 // Create book
$(".js-create-offlineStatus").click(loadOfflineStatusForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#offlineStatus-table").on("click", ".js-update-offlineStatus", loadOfflineStatusForm);

$("#modal-offlineStatus").on("click", ".js-offlineStatus-update-form", saveOfflineStatusForm);
// Delete book
// $("#offlineStatus-table").on("click", ".js-delete-offlineStatus", loadOfflineStatusForm);
// $("#modal-offlineStatus").on("click", ".js-offlineStatus-delete-form", deleteOfflineStatusForm);

});
