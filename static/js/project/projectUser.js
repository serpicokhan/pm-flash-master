$(function () {

  var loadProjectUserForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-projectUser").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-projectUser .modal-content").html(data.html_projectUser_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveProjectUserForm= function () {

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
         $("#tbody_projectUser").empty();
         $("#tbody_projectUser").html(data.html_projectUser_list);
         $("#modal-projectUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#projectUser-table tbody").html(data.html_projectUser_list);
         $("#modal-projectUser .modal-content").html(data.html_projectUser_form);
       }
     }
   });
   return false;
 };
 var deleteProjectUserForm= function (event) {
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
          console.log(data);
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_projectUser").empty();
          $("#tbody_projectUser").html(data.html_projectUser_list);
          $('#modal-projectUser').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          // $("#task-table tbody").html(data.html_task_list);
          // $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };



 // Create book
$(".js-create-projectUser").unbind();
$(".js-create-projectUser").click(loadProjectUserForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#projectUser-table").on("click", ".js-update-projectUser", loadProjectUserForm);

$("#modal-projectUser").on("submit", ".js-projectUser-update-form", loadProjectUserForm);
// Delete book
$("#projectUser-table").on("click", ".js-delete-projectUser", loadProjectUserForm);
$("#modal-projectUser").on("submit", ".js-projectUser-delete-form", saveProjectUserForm);
$("#modal-projectUser").on("click", ".js-projectUser-delete-form", deleteProjectUserForm);
});
