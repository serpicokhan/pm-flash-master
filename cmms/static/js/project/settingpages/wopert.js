$(function () {

  var loadWoPertForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woPert").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-woPert .modal-content").html(data.html_woPert_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoPertForm= function () {


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
         $("#tbody_woPert").empty();
         $("#tbody_woPert").html(data.html_woPert_list);
         $("#modal-woPert").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woPert-table tbody").html(data.html_woPert_list);
         $("#modal-woPert .modal-content").html(data.html_woPert_form);
       }
     }
   });
   return false;
 };
 var deleteWoPertForm= function (event) {

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
          $("#tbody_woPert").empty();
          $("#tbody_woPert").html(data.html_woPert_list);
          $("#modal-woPert").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woPert-table tbody").html(data.html_woPert_list);
          $("#modal-woPert .modal-content").html(data.html_woPert_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-woPert").click(loadWoPertForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woPert-table").on("click", ".js-update-woPert", loadWoPertForm);

$("#modal-woPert").on("click", ".js-woPert-update-form", saveWoPertForm);
// Delete book
$("#woPert-table").on("click", ".js-delete-woPert", loadWoPertForm);
$("#modal-woPert").on("click", ".js-woPert-delete-form", deleteWoPertForm);

});
