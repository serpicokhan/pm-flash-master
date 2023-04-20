$(function () {

  var loadAssetPurchaseForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetPurchase").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetPurchase .modal-content").html(data.html_assetPurchase_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetPurchaseForm= function () {

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
         $("#tbody_assetPurchase").empty();
         $("#tbody_assetPurchase").html(data.html_assetPurchase_list);
         $("#modal-assetPurchase").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetPurchase-table tbody").html(data.html_assetPurchase_list);
         $("#modal-assetPurchase .modal-content").html(data.html_assetPurchase_form);
       }
     }
   });
   return false;
 };
 var deleteAssetPurchaseForm= function (event) {
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
          $("#tbody_assetPurchase").empty();
          $("#tbody_assetPurchase").html(data.html_assetPurchase_list);
          $("#modal-assetPurchase").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetPurchase-table tbody").html(data.html_assetPurchase_list);
          $("#modal-assetPurchase .modal-content").html(data.html_assetPurchase_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-assetPurchase").unbind();
$(".js-create-assetPurchase").click(loadAssetPurchaseForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetPurchase-table").on("click", ".js-update-assetPurchase", loadAssetPurchaseForm);

$("#modal-assetPurchase").on("submit", ".js-assetPurchase-update-form", loadAssetPurchaseForm);
// Delete book
$("#assetPurchase-table").on("click", ".js-delete-assetPurchase", loadAssetPurchaseForm);
$("#modal-assetPurchase").on("click", ".js-assetPurchase-delete-form", deleteAssetPurchaseForm);

});
