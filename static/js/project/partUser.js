$(function () {

  var loadPartUserForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-partUser").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-partUser .modal-content").html(data.html_partUser_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savePartUserForm= function () {

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
         $("#tbody_partUser").empty();
         $("#tbody_partUser").html(data.html_partUser_list);
         $("#modal-partUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partUser-table tbody").html(data.html_partUser_list);
         $("#modal-partUser .modal-content").html(data.html_partUser_form);
       }
     }
   });
   return false;
 };
 var deletePartUserForm= function (event) {
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
          $("#tbody_partUser").empty();
          $("#tbody_partUser").html(data.html_partUser_list);
          $("#modal-partUser").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#partUser-table tbody").html(data.html_partUser_list);
          $("#modal-partUser .modal-content").html(data.html_partUser_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-partUser").unbind();
$(".js-create-partUser").click(loadPartUserForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#partUser-table").on("click", ".js-update-partUser", loadPartUserForm);

$("#modal-partUser").on("submit", ".js-partUser-update-form", loadPartUserForm);
// Delete book
$("#partUser-table").on("click", ".js-delete-partUser", loadPartUserForm);
$("#modal-partUser").on("click", ".js-partUser-delete-form", deletePartUserForm);

});
