$(function () {

  var loadWoMeterForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woMeter").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-woMeter .modal-content").html(data.html_woMeter_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveWoMeterForm= function () {

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
         $("#tbody_woMeter").empty();
         $("#tbody_woMeter").html(data.html_woMeter_list);
         $("#modal-woMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woMeter-table tbody").html(data.html_woMeter_list);
         $("#modal-woMeter .modal-content").html(data.html_woMeter_form);
       }
     }
   });
   return false;
 };
 var deleteWoMeterForm= function (event) {

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
          $("#tbody_woMeter").empty();
          $("#tbody_woMeter").html(data.html_woMeter_list);
          $("#modal-woMeter").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woMeter-table tbody").html(data.html_woMeter_list);
          $("#modal-woMeter .modal-content").html(data.html_woMeter_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
// $(".js-create-woMeter").unbind();
$(".js-create-woMeter").click(loadWoMeterForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woMeter-table").on("click", ".js-update-woMeter", loadWoMeterForm);

$("#modal-woMeter").on("submit", ".js-woMeter-update-form", loadWoMeterForm);
// Delete book
$("#woMeter-table").on("click", ".js-delete-woMeter", loadWoMeterForm);
$("#modal-woMeter").on("click", ".js-woMeter-delete-form", deleteWoMeterForm);

});
