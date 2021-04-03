$(function () {

  var loadScheduleForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-schedule").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-schedule .modal-content").html(data.html_schedule_form);
        $('#id_shStartDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });
                    $('#id_shEndDate').pDatepicker({
                      format: 'YYYY-MM-DD',
                      initialValueType: 'gregorian',
                      autoClose:true


                  });//id_dateCompleted


      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveScheduleForm= function () {

   var form = $(this);
   $.ajax({
     async: true,
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     //beforeSend:function
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_schedule").empty();
         $("#tbody_schedule").html(data.html_schedule_list);
         $("#modal-schedule").modal("hide");

         //console.log(data.html_wo_list);
       }
       else {

         $("#schedule-table tbody").html(data.html_schedule_list);
         $("#modal-schedule .modal-content").html(data.html_schedule_form);
       }
     }
   });
   return false;
 };
 var deleteSchedule= function () {

    var form = $(this);
    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      //beforeSend:function
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_schedule").empty();
          $("#tbody_schedule").html(data.html_schedule_list);
          $("#modal-schedule").modal("hide");

          //console.log(data.html_wo_list);
        }
        else {

          $("#schedule-table tbody").html(data.html_schedule_list);
          $("#modal-schedule .modal-content").html(data.html_schedule_form);
        }
      }
    });
    return false;
  };

 // Create book
$(".js-create-schedule").unbind();
$(".js-create-schedule").click(loadScheduleForm);
//$("#schedule-submit").on("", ".js-schedule-create-form", saveScheduleForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#schedule-table").on("click", ".js-update-schedule", loadScheduleForm);

//$("#modal-schedule").on("submit", ".js-schedule-update-form", loadScheduleForm);
// Delete book
$("#schedule-table").on("click", ".js-delete-schedule", loadScheduleForm);
$("#modal-schedule").on("click", ".js-schedule-delete-form",deleteSchedule);

});
