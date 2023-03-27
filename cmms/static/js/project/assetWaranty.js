$(function () {

  var loadAssetWarantyForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetWaranty").modal({backdrop: 'static', keyboard: false});;
      },
      success: function (data) {
        $("#modal-assetWaranty .modal-content").html(data.html_assetWaranty_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetWarantyForm= function () {

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
         $("#tbody_assetWaranty").empty();
         $("#tbody_assetWaranty").html(data.html_assetWaranty_list);
         $("#modal-assetWaranty").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetWaranty-table tbody").html(data.html_assetWaranty_list);
         $("#modal-assetWaranty .modal-content").html(data.html_assetWaranty_form);
       }
     }
   });
   return false;
 };
 var deleteAssetWarantyForm= function (event) {
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
          $("#tbody_assetWaranty").empty();
          $("#tbody_assetWaranty").html(data.html_assetWaranty_list);
          $('#modal-assetWaranty').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          $("#assetWaranty-table tbody").html(data.html_assetWaranty_list);
          $("#modal-assetWaranty .modal-content").html(data.html_assetWaranty_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-assetWaranty").unbind();
$(".js-create-assetWaranty").click(loadAssetWarantyForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetWaranty-table").on("click", ".js-update-assetWaranty", loadAssetWarantyForm);

$("#modal-assetWaranty").on("submit", ".js-assetWaranty-update-form", loadAssetWarantyForm);
// Delete book
$("#assetWaranty-table").on("click", ".js-delete-assetWaranty", loadAssetWarantyForm);
$("#modal-assetWaranty").on("click", ".js-assetWaranty-delete-form", deleteAssetWarantyForm);

});
