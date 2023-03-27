
$(function () {


var loadForm =function (btn1) {

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
        $("#modal-report .modal-content").html('');
      },
      success: function (data) {

        $("#modal-report .modal-content").html(data.html_report_form);


      }
    });



};
var loadFormReports =function (btn1) {

  var btn=0;
  //console.log(btn1);
  if($(btn1).attr("type")=="click")
   btn=$(this);
  else {
    btn=btn1;
  }

  return $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

      $("#modal-simplereport").modal("show");
    },
    success: function (data) {
      // alert("success");

      $("#modal-simplereport .modal-content").html(data.html_simpleReport_form);
      $('.selectpicker').selectpicker();
      $('.datepicker').pDatepicker({
        format: 'YYYY-MM-DD',

        autoClose:true,
        initialValueType: 'gregorian'
                  });//id_dateCompleted

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




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoReportLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadFdsdsorm(btn)).done(initReportFileLoad,initReportAssetLoad,initReportPartLoad );
   loadForm(btn);

   //initLoad();
 }
 var myReportLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoReportLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadFdsdsorm(btn)).done(initReportFileLoad,initReportAssetLoad,initReportPartLoad );
   loadFormReports(btn);

   //initLoad();
 }
var searchStr=function(){
  var str=$("#reportSearch").val()
  if(str.length==0)
    str='empty_'
  str=str.replace(' ','_')
  $.ajax({
    url: '/Report/'+str+'/reportSearch/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      console.log(data);

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_report").empty();
        $("#tbody_report").html(data.html_report_list);
        $(".woPaging").html(data.html_report_paginator);
        // $("#report-table").on("click", ".js-update-report", myReportLoader);
        // $("#modal-report").modal("hide");
       // console.log(data.html_report_list);

    }
  });
  return false;

}
$("#reportSearch").on('input',function(){
  searchStr();

}
);
$("#reportCategory").change(function(){
  $.ajax({
    url: '/Report/'+$("#reportCategory").val()+'/FilterCategory/',

    type: 'get',
    dataType: 'json',
    success: function (data) {

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_report").empty();
        $("#tbody_report").html(data.html_report_list);
        // console.log("start");
        // console.log(data);
        // console.log(data.html_report_paginator);
        $(".woPaging").html(data.html_report_paginator);
        // $("#report-table").on("click", ".js-update-report", myReportLoader);
        // $("#modal-report").modal("hide");
       // console.log(data.html_report_list);

    }
  });
  return false;
});
$("#option1").change(function(){
  $.ajax({
    url: '/Report/1/show_fav_reports/',

    type: 'get',
    dataType: 'json',
    success: function (data) {

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_report").empty();
        $("#tbody_report").html(data.html_report_list);
        // console.log("start");
        // console.log(data);
        // console.log(data.html_report_paginator);
        $(".woPaging").html(data.html_report_paginator);
        // $("#report-table").on("click", ".js-update-report", myReportLoader);
        // $("#modal-report").modal("hide");
       // console.log(data.html_report_list);

    }
  });
  return false;

});
$("#option2").change(function(){
  $.ajax({
    url: '/Report/0/show_fav_reports/',

    type: 'get',
    dataType: 'json',
    success: function (data) {

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_report").empty();
        $("#tbody_report").html(data.html_report_list);
        // console.log("start");
        // console.log(data);
        // console.log(data.html_report_paginator);
        $(".woPaging").html(data.html_report_paginator);
        // $("#report-table").on("click", ".js-update-report", myReportLoader);
        // $("#modal-report").modal("hide");
       // console.log(data.html_report_list);

    }
  });
  return false;

});
var make_fav=function(){
  // alert("123");
  var btn=$(this);
  report_id=$(this).attr("data-url");
  // console.log(report_id);
  $.ajax({
    url: '/Report/'+report_id+'/fav_report/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
    // console.log(data);
      btn.toggleClass("btn-info");
      btn.children('i').toggleClass("fa-star-o");




    },
    error:function(x,y,z){
      console.log(x,y,z);
    }
  });
  return false;
}
$(".js-create-report").click(myWoLoader);
$("#modal-report").on("submit", ".js-report-create-form", saveForm);

// Update book
$("#report-table").on("click", ".js-update-report", myReportLoader);
$("#report-table").on("click", ".fav_report", make_fav);
$("#report-table").on("click", ".js-operate-report", myReportLoader);
$("#modal-report").on("submit", ".js-report-update-form", saveForm);
// Delete book
$("#report-table").on("click", ".js-delete-report", loadForm);
$("#modal-report").on("submit", ".js-report-delete-form", saveForm);
//$("#report-table").on("click", ".js-update-wo", initxLoad);
});
