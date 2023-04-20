$(function () {

  var loadAssetMeterTemplateForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetMeterTemplate").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetMeterTemplate .modal-content").html(data.html_assetMeterTemplate_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetMeterTemplateForm= function () {

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
         $("#tbody_assetMeterTemplate").empty();
         $("#tbody_assetMeterTemplate").html(data.html_assetMeterTemplate_list);
         $("#modal-assetMeterTemplate").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetMeterTemplate-table tbody").html(data.html_assetMeterTemplate_list);
         $("#modal-assetMeterTemplate .modal-content").html(data.html_assetMeterTemplate_form);
       }
     }
   });
   return false;
 };
 var deleteAssetMeterTemplateForm= function (event) {
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
          $("#tbody_assetMeterTemplate").empty();
          $("#tbody_assetMeterTemplate").html(data.html_assetMeterTemplate_list);
          $('#modal-assetMeterTemplate').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {
          //
          // $("#task-table tbody").html(data.html_task_list);
          // $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };



 // Create book
$(".js-create-assetMeterTemplate").unbind();
$(".js-create-assetMeterTemplate").click(loadAssetMeterTemplateForm);
$("#assetMeterTemplate-table").on("click", ".js-update-assetMeterTemplate", loadAssetMeterTemplateForm);
$("#modal-assetMeterTemplate").on("submit", ".js-assetMeterTemplate-update-form", loadAssetMeterTemplateForm);
// Delete book
$("#assetMeterTemplate-table").on("click", ".js-delete-assetMeterTemplate", loadAssetMeterTemplateForm);
$("#modal-assetMeterTemplate").on("click", ".js-assetMeterTemplate-delete-form", deleteAssetMeterTemplateForm);

});
