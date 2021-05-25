$(function () {

  var loadWoCauseForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woCause").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-woCause .modal-content").html(data.html_woCause_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoCauseForm= function () {


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
         $("#tbody_woCause").empty();
         $("#tbody_woCause").html(data.html_woCause_list);
         $("#modal-woCause").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woCause-table tbody").html(data.html_woCause_list);
         $("#modal-woCause .modal-content").html(data.html_woCause_form);
       }
     }
   });
   return false;
 };
 //////////////

   var deleteWoCause=function(id){
     $.ajax({
       async: true,
       url: '/SettingPage/WoCause/'+id+'/Delete/',

       type: 'get',
       dataType: 'json',
       success: function (data) {
         console.log(data);
         if (data.form_is_valid) {
           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           $("#tbody_woCause").empty();
           $("#tbody_woCause").html(data.html_woCause_list);
           $("#modal-woCause").modal("hide");
           //console.log(data.html_wo_list);
         }
         else {

           $("#woCause-table tbody").html(data.html_woCause_list);
           $("#modal-woCause .modal-content").html(data.html_woCause_form);
         }
       }
     });

     return false;
   }
   $('#woCause-table').on('click','.js-delete-woCause', function () {
   const dashassetid=($(this).attr('data-url'));

     swal({
       title: "حذف",
       text: "حذف",
       type: "warning",
       showCancelButton: true,
       confirmButtonColor: "#DD6B55",
       confirmButtonText: "بلی",
       cancelButtonText: "خیر",
       closeOnConfirm: true
      }, function () {
          // cancelform();
          deleteWoCause(dashassetid);

      });

     // do something…
   });



 ///////////////

 // Create book
$(".js-create-woCause").click(loadWoCauseForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woCause-table").on("click", ".js-update-woCause", loadWoCauseForm);

$("#modal-woCause").on("click", ".js-woCause-update-form", saveWoCauseForm);
// Delete book
// $("#woCause-table").on("click", ".js-delete-woCause", loadWoCauseForm);
// $("#modal-woCause").on("click", ".js-woCause-delete-form", deleteWoCauseForm);

});
