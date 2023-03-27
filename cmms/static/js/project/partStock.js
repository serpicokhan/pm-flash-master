$(function () {

  var loadPartStockForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        // $("#modal-partStock").modal("show");
          $("#modal-partStock").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-partStock .modal-content").html(data.html_partStock_form);
        $('.selectpicker').selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savePartStockForm= function () {

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
         $("#tbody_partStock").empty();
         $("#tbody_partStock").html(data.html_partStock_list);
         $("#modal-partStock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partStock-table tbody").html(data.html_partStock_list);
         $("#modal-partStock .modal-content").html(data.html_partStock_form);
       }
     }
   });
   return false;
 };
 var deletePartStockForm= function (event) {
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
          $("#tbody_partStock").empty();
          $("#tbody_partStock").html(data.html_partStock_list);
          $("#modal-partStock").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#partStock-table tbody").html(data.html_partStock_list);
          $("#modal-partStock .modal-content").html(data.html_partStock_form);
        }
      }
    });
  }
    return false;
  };
 // Create book
$(".js-create-partStock").unbind();
$(".js-create-partStock").click(loadPartStockForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#partStock-table").on("click", ".js-update-partStock", loadPartStockForm);

$("#modal-partStock").on("submit", ".js-partStock-update-form", loadPartStockForm);
// Delete book
$("#partStock-table").on("click", ".js-delete-partStock", loadPartStockForm);
$("#modal-partStock").on("click", ".js-partStock-delete-form", deletePartStockForm);

});
