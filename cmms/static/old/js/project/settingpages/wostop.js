$(function () {

  var loadWoStopForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woStop").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-woStop .modal-content").html(data.html_woStop_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoStopForm= function () {


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
         $("#tbody_woStop").empty();
         $("#tbody_woStop").html(data.html_woStop_list);
         $("#modal-woStop").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woStop-table tbody").html(data.html_woStop_list);
         $("#modal-woStop .modal-content").html(data.html_woStop_form);
       }
     }
   });
   return false;
 };
 var deleteWoStopForm= function (event) {

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
          $("#tbody_woStop").empty();
          $("#tbody_woStop").html(data.html_woStop_list);
          $("#modal-woStop").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woStop-table tbody").html(data.html_woStop_list);
          $("#modal-woStop .modal-content").html(data.html_woStop_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-woStop").click(loadWoStopForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woStop-table").on("click", ".js-update-woStop", loadWoStopForm);

$("#modal-woStop").on("click", ".js-woStop-update-form", saveWoStopForm);
// Delete book
$("#woStop-table").on("click", ".js-delete-woStop", loadWoStopForm);
$("#modal-woStop").on("click", ".js-woStop-delete-form", deleteWoStopForm);

});
