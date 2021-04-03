$(function () {

  var loadWoActionForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woAction").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-woAction .modal-content").html(data.html_woAction_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoActionForm= function () {


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
         $("#tbody_woAction").empty();
         $("#tbody_woAction").html(data.html_woAction_list);
         $("#modal-woAction").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woAction-table tbody").html(data.html_woAction_list);
         $("#modal-woAction .modal-content").html(data.html_woAction_form);
       }
     }
   });
   return false;
 };
 var deleteWoActionForm= function (event) {

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
          $("#tbody_woAction").empty();
          $("#tbody_woAction").html(data.html_woAction_list);
          $("#modal-woAction").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woAction-table tbody").html(data.html_woAction_list);
          $("#modal-woAction .modal-content").html(data.html_woAction_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-woAction").click(loadWoActionForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woAction-table").on("click", ".js-update-woAction", loadWoActionForm);

$("#modal-woAction").on("click", ".js-woAction-update-form", saveWoActionForm);
// Delete book
$("#woAction-table").on("click", ".js-delete-woAction", loadWoActionForm);
$("#modal-woAction").on("click", ".js-woAction-delete-form", deleteWoActionForm);

});
