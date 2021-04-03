$(function () {

  var loadWoProblemForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woProblem").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-woProblem .modal-content").html(data.html_woProblem_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoProblemForm= function () {


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
         $("#tbody_woProblem").empty();
         $("#tbody_woProblem").html(data.html_woProblem_list);
         $("#modal-woProblem").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woProblem-table tbody").html(data.html_woProblem_list);
         $("#modal-woProblem .modal-content").html(data.html_woProblem_form);
       }
     }
   });
   return false;
 };
 var deleteWoProblemForm= function (event) {

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
          $("#tbody_woProblem").empty();
          $("#tbody_woProblem").html(data.html_woProblem_list);
          $("#modal-woProblem").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woProblem-table tbody").html(data.html_woProblem_list);
          $("#modal-woProblem .modal-content").html(data.html_woProblem_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-woProblem").click(loadWoProblemForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woProblem-table").on("click", ".js-update-woProblem", loadWoProblemForm);

$("#modal-woProblem").on("click", ".js-woProblem-update-form", saveWoProblemForm);
// Delete book
$("#woProblem-table").on("click", ".js-delete-woProblem", loadWoProblemForm);
$("#modal-woProblem").on("click", ".js-woProblem-delete-form", deleteWoProblemForm);

});
