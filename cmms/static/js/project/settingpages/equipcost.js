$(function () {

  var loadEquipCostForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        // alert(btn.attr("data-url"));
        $("#modal-equipCost").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-equipCost .modal-content").html(data.html_equipCost_form);
    // $('.selectpicker').selectpicker();


      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveEquipCostForm= function () {


   var form = $(this).parent();
   $.ajax({
     async: true,
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_equipCost").empty();
         $("#tbody_equipCost").html(data.html_equipCost_list);
         $("#modal-equipCost").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#equipCost-table tbody").html(data.html_equipCost_list);
         $("#modal-equipCost .modal-content").html(data.html_equipCost_form);
       }
     }
   });
   return false;
 };
 var deleteEquipCostForm= function (event) {

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
          $("#tbody_equipCost").empty();
          $("#tbody_equipCost").html(data.html_equipCost_list);
          $("#modal-equipCost").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#equipCost-table tbody").html(data.html_equipCost_list);
          $("#modal-equipCost .modal-content").html(data.html_equipCost_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-equipCost").click(loadEquipCostForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#equipCost-table").on("click", ".js-update-equipCost", loadEquipCostForm);

$("#modal-equipCost").on("click", ".js-equipCost-update-form", saveEquipCostForm);
// Delete book
$("#equipCost-table").on("click", ".js-delete-equipCost", loadEquipCostForm);
$("#modal-equipCost").on("click", ".js-equipCost-delete-form", deleteEquipCostForm);

});
