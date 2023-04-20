$(function () {

  var loadAssetUserForm =function () {

    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetUser").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetUser .modal-content").html(data.html_assetUser_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetUserForm= function () {

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
         $("#tbody_assetUser").empty();
         $("#tbody_assetUser").html(data.html_assetUser_list);
         $("#modal-assetUser").modal("hide");

         //console.log(data.html_wo_list);
       }
       else {

         $("#assetUser-table tbody").html(data.html_assetUser_list);
         $("#modal-assetUser .modal-content").html(data.html_assetUser_form);
       }
     }
   });
   return false;
 };
 var deleteAssetUserForm= function (event) {
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
          $("#tbody_assetUser").empty();
          $("#tbody_assetUser").html(data.html_assetUser_list);
          $("#modal-assetUser").modal("hide");

          //console.log(data.html_wo_list);
        }
        else {

          $("#task-table tbody").html(data.html_assetUser_list);
          $("#modal-task .modal-content").html(data.html_assetUser_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-assetUser").unbind();
$(".js-create-assetUser").click(loadAssetUserForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetUser-table").on("click", ".js-update-assetUser", loadAssetUserForm);

$("#modal-assetUser").on("submit", ".js-assetUser-update-form", loadAssetUserForm);
// Delete book
$("#assetUser-table").on("click", ".js-delete-assetUser", loadAssetUserForm);
$("#modal-assetUser").on("click", ".js-assetUser-delete-form", deleteAssetUserForm);

});
