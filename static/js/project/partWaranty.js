$(function () {

  var loadPartWarantyForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-partWaranty").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-partWaranty .modal-content").html(data.html_partWaranty_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savePartWarantyForm= function () {

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
         $("#tbody_partWaranty").empty();
         $("#tbody_partWaranty").html(data.html_partWaranty_list);
         $("#modal-partWaranty").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partWaranty-table tbody").html(data.html_partWaranty_list);
         $("#modal-partWaranty .modal-content").html(data.html_partWaranty_form);
       }
     }
   });
   return false;
 };
 var deletePartWarantyForm= function (event) {
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
          $("#tbody_partWaranty").empty();
          $("#tbody_partWaranty").html(data.html_partWaranty_list);
          $("#modal-partWaranty").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#partWaranty-table tbody").html(data.html_partWaranty_list);
          $("#modal-partWaranty .modal-content").html(data.html_partWaranty_form);
        }
      }
    });
  }
    return false;
  };
 // Create book
$(".js-create-partWaranty").unbind();
$(".js-create-partWaranty").click(loadPartWarantyForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#partWaranty-table").on("click", ".js-update-partWaranty", loadPartWarantyForm);

$("#modal-partWaranty").on("submit", ".js-partWaranty-update-form", loadPartWarantyForm);
// Delete book
$("#partWaranty-table").on("click", ".js-delete-partWaranty", loadPartWarantyForm);
$("#modal-partWaranty").on("submit", ".js-partWaranty-delete-form", savePartWarantyForm);
$("#modal-partWaranty").on("click", ".js-partWaranty-delete-form", deletePartWarantyForm);

});
