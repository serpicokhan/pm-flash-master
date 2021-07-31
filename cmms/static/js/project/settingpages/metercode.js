$(function () {

  var loadMeterCodeForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-meterCode").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-meterCode .modal-content").html(data.html_meterCode_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveMeterCodeForm= function () {


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
         $("#tbody_meterCode").empty();
         $("#tbody_meterCode").html(data.html_meterCode_list);
         $("#modal-meterCode").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#meterCode-table tbody").html(data.html_meterCode_list);
         $("#modal-meterCode .modal-content").html(data.html_meterCode_form);
       }
     }
   });
   return false;
 };
 var deleteMeterCodeForm= function (event) {

    var form = $(this);
    if(event.target.className=="btn btn-danger")
    {
    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_meterCode").empty();
          $("#tbody_meterCode").html(data.html_meterCode_list);
          $("#modal-meterCode").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#meterCode-table tbody").html(data.html_meterCode_list);
          $("#modal-meterCode .modal-content").html(data.html_meterCode_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-meterCode").click(loadMeterCodeForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#meterCode-table").on("click", ".js-update-meterCode", loadMeterCodeForm);

$("#modal-meterCode").on("click", ".js-meterCode-update-form", saveMeterCodeForm);
// Delete book
$("#meterCode-table").on("click", ".js-delete-meterCode", loadMeterCodeForm);
$("#modal-meterCode").on("click", ".js-meterCode-delete-form", deleteMeterCodeForm);

});
