$(function () {

  var loadWoMiscForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woMisc").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-woMisc .modal-content").html(data.html_woMisc_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoMiscForm= function () {

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
         $("#tbody_woMisc").empty();
         $("#tbody_woMisc").html(data.html_woMisc_list);
         $("#modal-woMisc").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woMisc-table tbody").html(data.html_woMisc_list);
         $("#modal-woMisc .modal-content").html(data.html_woMisc_form);
       }
     }
   });
   return false;
 };

 var deleteWoMiscForm= function (event) {

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
          $("#tbody_woMisc").empty();
          $("#tbody_woMisc").html(data.html_woMisc_list);
          $("#modal-woMisc").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woMisc-table tbody").html(data.html_woMisc_list);
          $("#modal-woMisc .modal-content").html(data.html_woMisc_form);
        }
      }
    });
  }
    return false;
  };


 // Create book
$(".js-create-woMisc").unbind();
$(".js-create-woMisc").click(loadWoMiscForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woMisc-table").on("click", ".js-update-woMisc", loadWoMiscForm);

$("#modal-woMisc").on("submit", ".js-woMisc-update-form", loadWoMiscForm);
// Delete book
$("#woMisc-table").on("click", ".js-delete-woMisc", loadWoMiscForm);
$("#modal-woMisc").on("click", ".js-woMisc-delete-form", deleteWoMiscForm);

});
