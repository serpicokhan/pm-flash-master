$(function () {

  var loadTaskTemplateForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-taskTemplate").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        $("#modal-taskTemplate .modal-content").html(data.html_taskTemplate_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveTaskTemplateForm= function () {

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
         $("#tbody_taskTemplate").empty();
         $("#tbody_taskTemplate").html(data.html_taskTemplate_list);
         $('#modal-taskTemplate').modal('hide');
         alert("123");
         //console.log(data.html_wo_list);
       }
       else {


         $("#taskTemplate-table tbody").html(data.html_taskTemplate_list);
         $("#modal-taskTemplate .modal-content").html(data.html_taskTemplate_form);

       }
     }
   });
   return false;
 };

 var deleteTaskTemplateForm= function (event) {
   console.log(event.target.className);
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
          $("#tbody_taskTemplate").empty();
          $("#tbody_taskTemplate").html(data.html_taskTemplate_list);
          $('#modal-taskTemplate').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          $("#taskTemplate-table tbody").html(data.html_taskTemplate_list);
          $("#modal-taskTemplate .modal-content").html(data.html_taskTemplate_form);
        }
      }
    });
  }
    return false;
  };




 // Create book
$(".js-create-taskTemplate").click(loadTaskTemplateForm);
$("#taskTemplate-table").on("click", ".js-update-taskTemplate", loadTaskTemplateForm);
// $("#modal-taskTemplate").on("submit", ".js-taskTemplate-update-form", saveTaskTemplateForm);
// Delete book
$("#taskTemplate-table").on("click", ".js-delete-taskTemplate", loadTaskTemplateForm);
$("#modal-taskTemplate").on("click", ".js-taskTemplate-delete-form", deleteTaskTemplateForm);

});
