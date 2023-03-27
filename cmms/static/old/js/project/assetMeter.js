$(function () {

  var loadAssetMeterForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetMeter").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetMeter .modal-content").html(data.html_assetMeter_form);
         $('.selectpicker').selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetMeterForm= function () {

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
         $("#tbody_assetMeter").empty();
         $("#tbody_assetMeter").html(data.html_assetMeter_list);
         $("#modal-assetMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetMeter-table tbody").html(data.html_assetMeter_list);
         $("#modal-assetMeter .modal-content").html(data.html_assetMeter_form);
       }
     }
   });
   return false;
 };
 var deleteAssetMeterForm= function (event) {
   // console.log(event.target.className);
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
          $("#tbody_assetMeter").empty();
          $("#tbody_assetMeter").html(data.html_assetMeter_list);
          $('#modal-assetMeter').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          $("#task-table tbody").html(data.html_task_list);
          $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };


 // Create book
$(".js-create-assetMeter").unbind();
$(".js-create-assetMeter").click(loadAssetMeterForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetMeter-table").on("click", ".js-update-assetMeter", loadAssetMeterForm);

$("#modal-assetMeter").on("submit", ".js-assetMeter-update-form", loadAssetMeterForm);
// Delete book
$("#assetMeter-table").on("click", ".js-delete-assetMeter", loadAssetMeterForm);
// $("#modal-assetMeter").on("submit", ".js-assetMeter-delete-form", saveAssetMeterForm);
$("#modal-assetMeter").on("click", ".js-assetMeter-delete-form", deleteAssetMeterForm);

});
