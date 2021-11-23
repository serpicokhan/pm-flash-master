$(function () {

  var loadKpiExceptionForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-kpiException").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-kpiException .modal-content").html(data.html_kpiException_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveKpiExceptionForm= function () {


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
         $("#tbody_kpiException").empty();
         $("#tbody_kpiException").html(data.html_kpiException_list);
         $("#modal-kpiException").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#kpiException-table tbody").html(data.html_kpiException_list);
         $("#modal-kpiException .modal-content").html(data.html_kpiException_form);
       }
     }
   });
   return false;
 };

   var deleteKpiException=function(id){
     $.ajax({
       async: true,
       url: '/SettingPage/KpiException/'+id+'/Delete/',

       type: 'get',
       dataType: 'json',
       success: function (data) {
         console.log(data);
         if (data.form_is_valid) {
           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           $("#tbody_kpiException").empty();
           $("#tbody_kpiException").html(data.html_kpiException_list);
           $("#modal-kpiException").modal("hide");
           //console.log(data.html_wo_list);
         }
         else {

           $("#kpiException-table tbody").html(data.html_kpiException_list);
           $("#modal-kpiException .modal-content").html(data.html_kpiException_form);
         }
       }
     });

     return false;
   }
   $('#kpiException-table').on('click','.js-delete-kpiException', function () {
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
          deleteKpiException(dashassetid);

      });

     // do something…
   });

 /////////////////////////////

 // Create book
$(".js-create-kpiException").click(loadKpiExceptionForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#kpiException-table").on("click", ".js-update-kpiException", loadKpiExceptionForm);

$("#modal-kpiException").on("click", ".js-kpiException-update-form", saveKpiExceptionForm);
// Delete book
// $("#kpiException-table").on("click", ".js-delete-kpiException", loadKpiExceptionForm);
// $("#modal-kpiException").on("click", ".js-kpiException-delete-form", deleteKpiExceptionForm);

});
