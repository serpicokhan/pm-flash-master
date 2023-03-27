
$(function () {


  var loadFormReport =function (btn1) {

    var btn=0;
    //console.log(btn1);
    if($(btn1).attr("type")=="click")
     btn=$(this);
    else {
      btn=btn1;
    }
    //console.log($(btn).attr("type"));
    //console.log($(btn).attr("data-url"));
    return $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");
        // /$("#modal-report").modal("hide");
        $("#modal-report").modal("show");
      },
      success: function (data) {
        
        $("#modal-report .modal-content").html(data.html_report_form);


      }
    });



};
//$("#modal-report").on("submit", ".js-report-create-form",
var saveForm= function () {
   var form = $(this);

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_report").empty();
         $("#tbody_report").html(data.html_report_list);
         $("#modal-report").modal("hide");
        // console.log(data.html_report_list);
       }
       else {

         $("#report-table tbody").html(data.html_report_list);
         $("#modal-report .modal-content").html(data.html_report_form);
       }
     }
   });
   return false;
 };
/*
 $('#modal-report').on('hidden.bs.modal', function () {
   alert("321321");
   console.log($("#lastWorkOrderid").val());
   $.ajax({
     url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/deleteChildren',



     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_report").empty();
         //$("#tbody_report").html(data.html_wo_list);
         //$("#modal-report").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#report-table tbody").html(data.html_wo_list);
         $("#modal-report .modal-content").html(data.html_form);
       }
     }
   });


  // do something…
});
*/
 //alert("321312");
 // Create book




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoReportLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initReportFileLoad,initReportAssetLoad,initReportPartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-report").click(myWoLoader);
$("#modal-report").on("submit", ".js-report-create-form", saveForm);

// Update book
$("#report-table").on("click", ".js-update-report", myWoLoader);
$("#modal-report").on("submit", ".js-report-update-form", saveForm);
// Delete book
$("#report-table").on("click", ".js-delete-report", loadForm);
$("#modal-report").on("submit", ".js-report-delete-form", saveForm);
//$("#report-table").on("click", ".js-update-wo", initxLoad);
});
