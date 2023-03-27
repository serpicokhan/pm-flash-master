$(function () {

  var loadUserGroupForm =function () {

    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-userGroup").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {


        $("#modal-userGroup .modal-content").html(data.html_userGroup_form);
        // $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveUserGroupForm= function () {


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
         $("#tbody_userGroup").empty();
         $("#tbody_userGroup").html(data.html_userGroup_list);
         $("#modal-userGroup").modal("hide");

         //console.log(data.html_wo_list);
       }
       else {

         $("#userGroup-table tbody").html(data.html_userGroup_list);
         $("#modal-userGroup .modal-content").html(data.html_userGroup_form);
       }
     }
   });
   return false;
 };
 var deleteUserGroupForm= function (event) {

    var form = $(this);
    if(event.target.className=="btn btn-danger")
    {
    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_userGroup").empty();
          $("#tbody_userGroup").html(data.html_userGroup_list);
          $("#modal-userGroup").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#userGroup-table tbody").html(data.html_userGroup_list);
          $("#modal-userGroup .modal-content").html(data.html_userGroup_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-userGroup").click(loadUserGroupForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#userGroup-table").on("click", ".js-update-userGroup", loadUserGroupForm);

$("#modal-userGroup").on("click", ".js-userGroup-update-form", saveUserGroupForm);
// Delete book
$("#userGroup-table").on("click", ".js-delete-userGroup", loadUserGroupForm);
$("#modal-userGroup").on("click", ".js-userGroup-delete-form", deleteUserGroupForm);

});
