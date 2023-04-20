$(function () {

  var loadStockForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        
      },
      success: function (data) {
        $("#modal-stock .modal-content").html(data.html_stock_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveStockForm= function () {

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
         $("#tbody_stock").empty();
         $("#tbody_stock").html(data.html_stock_list);
         $("#modal-stock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#stock-table tbody").html(data.html_stock_list);
         $("#modal-stock .modal-content").html(data.html_stock_form);
       }
     }
   });
   return false;
 };

 // Create book
$(".js-create-stock").click(loadStockForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#stock-table").on("click", ".js-update-stock", loadStockForm);

$("#modal-stock").on("submit", ".js-stock-update-form", loadStockForm);
// Delete book
$("#stock-table").on("click", ".js-delete-stock", loadStockForm);
$("#modal-stock").on("submit", ".js-stock-delete-form", saveStockForm);

});
