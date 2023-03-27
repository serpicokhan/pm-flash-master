$(function () {

  var loadbusinessAssetForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-businessAsset").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-businessAsset .modal-content").html(data.html_businessAsset_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savebusinessAssetForm= function () {

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
         $("#tbody_businessAsset").empty();
         $("#tbody_businessAsset").html(data.html_businessAsset_list);
         $("#modal-businessAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessAsset-table tbody").html(data.html_businessAsset_list);
         $("#modal-businessAsset .modal-content").html(data.html_businessAsset_form);
       }
     }
   });
   return false;
 };

 // Create book
$(".js-create-businessAsset").unbind();
$(".js-create-businessAsset").click(loadbusinessAssetForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#businessAsset-table").on("click", ".js-update-businessAsset", loadbusinessAssetForm);

$("#modal-businessAsset").on("submit", ".js-businessAsset-update-form", loadbusinessAssetForm);
// Delete book
$("#businessAsset-table").on("click", ".js-delete-businessAsset", loadbusinessAssetForm);
$("#modal-businessAsset").on("submit", ".js-businessAsset-delete-form", savebusinessAssetForm);

});
