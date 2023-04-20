$(function () {

  var loadWoNotifyForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woNotify").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-woNotify .modal-content").html(data.html_woNotify_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoNotifyForm= function () {

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
         $("#tbody_woNotify").empty();
         $("#tbody_woNotify").html(data.html_woNotify_list);
         $("#modal-woNotify").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woNotify-table tbody").html(data.html_woNotify_list);
         $("#modal-woNotify .modal-content").html(data.html_woNotify_form);
       }
     }
   });
   return false;
 };

 var deleteWoNotifyForm= function (event) {

    var form = $(this)
    // console.log(form.attr());
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
          $("#tbody_woNotify").empty();
          $("#tbody_woNotify").html(data.html_woNotify_list);
          $("#modal-woNotify").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woNotify-table tbody").html(data.html_woNotify_list);
          $("#modal-woNotify .modal-content").html(data.html_woNotify_form);
        }
      }
    });
  }
    return false;
  };


 // Create book
$(".js-create-woNotify").unbind();
$(".js-create-woNotify").click(loadWoNotifyForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woNotify-table").on("click", ".js-update-woNotify", loadWoNotifyForm);

$("#modal-woNotify").on("submit", ".js-woNotify-update-form", loadWoNotifyForm);
// Delete book
$("#woNotify-table").on("click", ".js-delete-woNotify", loadWoNotifyForm);
$("#modal-woNotify").on("click", ".js-woNotify-delete-form", deleteWoNotifyForm);

});
