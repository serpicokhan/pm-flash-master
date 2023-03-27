$(function () {

  var loadPartBusinessForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-partBusiness").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-partBusiness .modal-content").html(data.html_partBusiness_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savePartBusinessForm= function () {

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
         $("#tbody_partBusiness").empty();
         $("#tbody_partBusiness").html(data.html_partBusiness_list);
         $("#modal-partBusiness").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partBusiness-table tbody").html(data.html_partBusiness_list);
         $("#modal-partBusiness .modal-content").html(data.html_partBusiness_form);
       }
     }
   });
   return false;
 };

 // Create book
$(".js-create-partBusiness").unbind();
$(".js-create-partBusiness").click(loadPartBusinessForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#partBusiness-table").on("click", ".js-update-partBusiness", loadPartBusinessForm);

$("#modal-partBusiness").on("submit", ".js-partBusiness-update-form", loadPartBusinessForm);
// Delete book
$("#partBusiness-table").on("click", ".js-delete-partBusiness", loadPartBusinessForm);
$("#modal-partBusiness").on("submit", ".js-partBusiness-delete-form", savePartBusinessForm);

});
