$(function () {

  var loadPartLocationForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-partLocation").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-partLocation .modal-content").html(data.html_partLocation_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savePartLocationForm= function () {

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
         $("#tbody_partLocation").empty();
         $("#tbody_partLocation").html(data.html_partLocation_list);
         $("#modal-partLocation").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetPart-table tbody").html(data.html_partLocation_list);
         $("#modal-partLocation .modal-content").html(data.html_partLocation_form);
       }
     }
   });
   return false;
 };

 // Create book
$(".js-create-partLocation").unbind();
$(".js-create-partLocation").click(loadPartLocationForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#partLocation-table").on("click", ".js-update-partLocation", loadPartLocationForm);

$("#modal-partLocation").on("submit", ".js-partLocation-update-form", loadPartLocationForm);
// Delete book
$("#partLocation-table").on("click", ".js-delete-partLocation", loadPartLocationForm);
$("#modal-partLocation").on("submit", ".js-partLocation-delete-form", savePartLocationForm);

});
