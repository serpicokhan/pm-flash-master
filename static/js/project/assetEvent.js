$(function () {

  var loadAssetEventForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetEvent").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetEvent .modal-content").html(data.html_assetEvent_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetEventForm= function () {

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
         $("#tbody_assetEvent").empty();
         $("#tbody_assetEvent").html(data.html_assetEvent_list);
         $("#modal-assetEvent").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetEvent-table tbody").html(data.html_assetEvent_list);
         $("#modal-assetEvent .modal-content").html(data.html_assetEvent_form);
       }
     }
   });
   return false;
 };
 var deleteAssetEventForm= function (event) {
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
          $("#tbody_assetEvent").empty();
          $("#tbody_assetEvent").html(data.html_assetEvent_list);
          $('#modal-assetEvent').modal('hide');

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
$(".js-create-assetEvent").unbind();
$(".js-create-assetEvent").click(loadAssetEventForm);
$("#assetEvent-table").on("click", ".js-update-assetEvent", loadAssetEventForm);
$("#modal-assetEvent").on("submit", ".js-assetEvent-update-form", loadAssetEventForm);
// Delete book
$("#assetEvent-table").on("click", ".js-delete-assetEvent", loadAssetEventForm);
$("#modal-assetEvent").on("click", ".js-assetEvent-delete-form", deleteAssetEventForm);

});
