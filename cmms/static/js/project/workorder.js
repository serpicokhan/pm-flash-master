
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
        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {

        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_wo_form);
        $('#id_requiredCompletionDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });
                    $('#id_datecreated').pDatepicker({
                      format: 'YYYY-MM-DD',
                      initialValueType: 'gregorian',
                      autoClose:true


                  });//id_dateCompleted
                  //console.log($('#id_dateCompleted').val()+":dsadsa");

                                $('#id_dateCompleted').pDatepicker({
                                  format: 'YYYY-MM-DD',

                                  autoClose:true,
                                  initialValueType: 'gregorian'
                                            });//id_dateCompleted

                  //id_completedByUser

                  $("#id_woAsset").change(function(){
                    $.ajax({
                      url: $("#lastWorkOrderid").val()+'/'+$("#id_woAsset").val()+'/setAsset/',
                      type:'get',
                      dataType: 'json',
                      success: function (data) {
                        // console.log("hahaha");

                      }
                    });


                  });
                  $('.selectpicker').selectpicker();
                  $('.basicAutoComplete').autoComplete();
                  initLoad();
                  initWoPartLoad();
                  initWoMeterLoad();
                  initWoMiscLoad();
                  initWoNotifyLoad();
                  initWoFileLoad();initWoLogLoad();
                  initWoPertLoad();




      }

    });
   // $("#id_assignedToUser").chosen('.chosen-select-width': {
     //           width: "95%"
       //     });



};
var LoadFormSetEm =function () {
  matches=[];
  $(".selection-box:checked").each(function() {
      matches.push(this.value);
  });
  // console.log(matches);



  // return $.ajax({
  //   url: $(this).attr("date-url")+matches,
  //   type: 'get',
  //   dataType: 'json',
  //   beforeSend: function () {
  //
  //     $("#modal-woEM").modal({backdrop: 'static', keyboard: false});
  //
  //   },
  //   success: function (data) {
  //     //alert("3123@!");
  //     // alert(1);
  //     $("#modal-woEM .modal-content").html(data.modalem);
  //
  //
  //   }
  // });
  swal({
       title: "تبدیل به EM",
       text:"",
       type: "warning",
       showCancelButton: true,
       confirmButtonColor: "#DD6B55",
       confirmButtonText: "بلی",
       cancelButtonText: "خیر",
       closeOnConfirm: true
   }, function () {
     $.ajax({
       url: '/WorkOrder/bulkEm/'+matches,
       data: matches,
       type: 'get',
       dataType: 'json',
       success: function (data) {
         if (data.form_is_valid) {
           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           $("#tbody_company").empty();
           $("#tbody_company").html(data.html_wo_list);
           // alert("!23");
          $("#modal-woEM").modal("hide");
          // $("tr").on("click", showAssetDetails);

          // console.log(data.html_asset_list);
         }
         else {

           $("#company-table tbody").html(data.html_asset_list);
           $("#modal-assetcategory .modal-content").html(data.html_asset_form);
         }
       }
     });

   });




};
  var LoadFormsetDelete =function () {
    var matches = [];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    console.log(matches);


    return $.ajax({
      url: $(this).attr("data-url")+matches,
      type: 'get',
      // data: {'action[]': matches},



      beforeSend: function () {



        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {

        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_wo_form);





      }

    });




};

var cancelform=function(){

    return $.ajax({
      url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/cancel/',
      type: 'post',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        // alert("321321");


      },
      success: function (data) {
        // console.log(data);
        if(data.form_is_valid)
        {
          swal("حذف شد!", $("#id_summaryofIssue").val(), "success");



        }
        else {

        }

      }

    });

  }

//$("#modal-company").on("submit", ".js-company-create-form",
var saveForm= function () {

   var form = $(this);


   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(xhr,opt)
     {
      if(!$(this)[0].url.includes('delete')){
        if($("#id_woAsset").val().length<1)
        {
          toastr.error("برای دستور کار، تجهیزی انتخاب نشده است");
          xhr.abort();
        }
        if($("#id_summaryofIssue").val().length<1)
        {
          toastr.error("اطلاعات مربوط به خلاصه مشکل را وارد نمایید!");
          xhr.abort();
        }

        if($("#havetasks").val()=="-1")
        {
          toastr.error("فعالیتی مشخص نکرده اید!");
          xhr.abort();
        }



      }


     },
     success: function (data) {
       if (data.form_is_valid) {

         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $("#modal-company").modal("hide");
         toastr.success("دستور کار با موفقیت  ایجاد شد");
         $("#issavechanged").val("1");


        // console.log(data.html_wo_list);
       }
       else {



         if(data.form_err_code==1)
         {
           toastr.error(data.form_err_msg);
         }
         else {
           $("#company-table tbody").html(data.html_wo_list);
           $("#modal-company .modal-content").html(data.html_wo_form);
           toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");


         }

       }
     }
   });
   return false;
 };
var saveFormsetForm= function () {

   var form = $(this);

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(xhr,opt)
     {



     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("table").find("tr:gt(2)").remove();
         $(data.html_formset_list).insertAfter('table > tbody > tr:nth-child(1)');
          // $("table > tbody").html(data.html_formset_list);
         $("#modal-company").modal("hide");
         toastr.success("دستورکارها با موفقیت حذف شدند");


        // console.log(data.html_wo_list);
       }
       else {



         if(data.form_err_code==1)
         {
           toastr.error(data.form_err_msg);
         }
         else {
           $("#company-table tbody").html(data.html_wo_list);
           $("#modal-company .modal-content").html(data.html_wo_form);
           toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");


         }

       }
     }
   });
   return false;
 };
 //############# Time Change ############################
 var getListWorkorderLastTime= function (n) {

    myurl="";
    if(n===2)
      myurl='ListCurrentWeek';
    else if(n===3) {
      myurl='ListCurrentMonth';
    }
    else {
       myurl='ListCurrentDay';
    }

    $.ajax({
      url: myurl,

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

          $("#modal-company").modal("hide");
         // console.log(data.html_amar_list);
        }
        else {


        }
      },
      error: function (jqXHR, exception) {
        alert(exception);
        console.log(exception)
      }
    });
    return false;
  };
////////////////Search buttom click#############################
var searchWorkorderByTags= function (searchStr) {


   $.ajax({
     url: '/WorkOrder/'+searchStr+'/Search/',

     type: 'GET',
     dataType: 'json',
     success: function (data) {

       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();

         $("#tbody_company").html(data.html_wo_list);
         $(".woPaging").html(data.html_wo_paginator);

         // $("#modal-company").modal("hide");
        // console.log(data.html_amar_list);
       }
       else {


       }
     },
     error: function (jqXHR, exception) {
       alert(exception);
       console.log(exception)
     }
   });
   return false;
 };
 ///
 var filter= function (searchStr) {


    $.ajax({
      url: '/WorkOrder/'+$("#wodt1").val()+'/'+$("#wodt2").val()+'/0/'+$("#ordercol").val()+'/filter/'+$('#ordertype').val(),

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          console.log(data);
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

          // $("#modal-company").modal("hide");
         // console.log(data.html_amar_list);
        }
        else {


        }
      },
      error: function (jqXHR, exception) {
        alert(exception);
        console.log(jqXHR)
      }
    });
    return false;
  };
 /////////////////////////////
 function sleep(milliseconds) {
   const date = Date.now();
   let currentDate = null;
   do {
     currentDate = Date.now();
   } while (currentDate - date < milliseconds);
 }
 $('#woSearch').keyup(function(e){
   // setTimeout(() => {  console.log("World!"); }, 2000);
   // sleep(2000);
   console.log(e);
   // e.cancle();
   strTag=$("#woSearch").val();
   if(strTag.length==0)
    strTag='empty_';
  strTag=strTag.replace(' ','_');

  searchWorkorderByTags(strTag);
   //alert("salam");

});
////////////////////////////////////////////////////////////////
  //############# Time Radio Button هفته###################
  $('#option2').change(function(){

    getListWorkorderLastTime(2);
});
//################### ماه #####################
$('#option3').change(function(){

  getListWorkorderLastTime(3);
});

$('#option1').change(function(){

  getListWorkorderLastTime(1);
});

 var initLoad=function()
 {
   //alert("initload");
   $.ajax({

     url: '/Task/'+$("#lastWorkOrderid").val()+'/listTask',



     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_task").empty();
         $("#tbody_task").html(data.html_task_list);
         if(data.is_not_empty){
           $("#havetasks").val("1");
         }
         $("#modal-task").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#task-table tbody").html(data.html_task_list);
         $("#modal-task .modal-content").html(data.html_task_form);
       }
     }
   });


   return false;
 };


 var initWoPartLoad=function(){

   $.ajax({

     url: '/WoPart/'+$("#lastWorkOrderid").val()+'/listWoPart',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woPart_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_woPart").empty();
         $("#tbody_woPart").html(data.html_woPart_list);
         $("#modal-woPart").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woPart-table tbody").html(data.html_woPart_list);
         $("#modal-woPart .modal-content").html(data.html_woPart_form);
       }
     }
   });
return false;
 };
 var initWoMeterLoad=function(){

   $.ajax({

     url: '/WoMeter/'+$("#lastWorkOrderid").val()+'/listWoMeter',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woMeter_list);  // <-- This is just a placeholder for now for testing
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


 var initWoMiscLoad=function(){

   $.ajax({

     url: '/WoMisc/'+$("#lastWorkOrderid").val()+'/listWoMisc',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woMisc_list);  // <-- This is just a placeholder for now for testing
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

 var initWoNotifyLoad=function(){

   $.ajax({

     url: '/WoNotify/'+$("#lastWorkOrderid").val()+'/listWoNotify',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_woNotify").empty();
         $("#tbody_woNotify").html(data.html_woNotify_list);
         $("#modal-woNotify").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woNotify-table tbody").html(data.html_woNotify_list);
         $("#modal-woNotify .modal-content").html(data.html_woNotify_form);
       }
     }
   });
 return false;
 };
 var initWoPertLoad=function(){

   $.ajax({

     url: '/WoPert/'+$("#lastWorkOrderid").val()+'/listWoPert',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_woPert").empty();
         $("#tbody_woPert").html(data.html_woPert_list);
         $("#modal-woPert").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woPert-table tbody").html(data.html_woPert_list);
         $("#modal-woPert .modal-content").html(data.html_woPert_form);
       }
     }
   });
 return false;
 };


 var initWoFileLoad=function(){

   $.ajax({

     url: '/WoFile/'+$("#lastWorkOrderid").val()+'/listWoFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_woFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_woFile").empty();
         $("#tbody_woFile").html(data.html_woFile_list);
         $("#modal-woFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#woFile-table tbody").html(data.html_woFile_list);
         $("#modal-woFile .modal-content").html(data.html_woFile_form);
       }
     }
   });
 return false;
 };
 var initWoLogLoad=function(){


   $.ajax({

     url: '/WoLog/'+$("#lastWorkOrderid").val()+'/listWoLog/',



     success: function (data) {
       console.log(data);

       if (data.form_is_valid) {
         // alert("!23");


         $("#tbody_wolog").empty();
         $("#tbody_wolog").html(data.html_wolog_list);
         $("#modal-wolog").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {
         // alert("fdfds");

         $("#wolog-table tbody").html(data.html_woFile_list);
         // $("#modal-wolog .modal-content").html(data.html_woFile_form);
       }
     }
   });
 return false;
 };


var loadPdate=function()
{
  $('#id_requiredCompletionDate').pDatepicker({
                  format: 'YYYY-MM-DD',
                  autoClose: true,
                  initialValueType: 'gregorian'
              });
              $('#id_datecreated').pDatepicker({
                format: 'YYYY-MM-DD',
                timePicker: {
                    enabled: true
                },

                              autoClose: true,
                              initialValueType: 'gregorian'
                          });//id_dateCompleted
                          $('#id_dateCompleted').pDatepicker({
                            format: 'YYYY-MM-DD',
                            timePicker: {
                                enabled: true
                            },
                            autoClose:true,
                                          initialValueType: 'gregorian'
                                      });//id_dateCompleted

}

 var myWoLoader= function(){
   btn=$(this);
   //console.log(btn);
   // $.when(loadForm(btn)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad,initWoPertLoad);

   //loadForm(btn);

   //initLoad();
 }
 var filterWo=function(id){
   return $.ajax({
     url: '/WorkOrder/'+id+'/getType/',
     type: 'get',
     dataType: 'json',
     beforeSend: function () {
       //alert(btn.attr("data-url"));
       //alert("321321");


     },
     success: function (data) {
       console.log(data);
       if(data.form_is_valid)
       {
         // alert("!23");

         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $(".woPaging").html(data.html_wo_paginator)

       }

     }

   });
 }

 $("#woType").change(function(){
   filterWo($("#woType").val());
 });
 //////////////////////////////////////////////
 var filterWoGroup=function(id){
   return $.ajax({
     url: '/WorkOrder/'+id+'/getGroup/',
     type: 'get',
     dataType: 'json',
     beforeSend: function () {
       //alert(btn.attr("data-url"));
       //alert("321321");


     },
     success: function (data) {
       console.log(data);
       if(data.form_is_valid)
       {
         // alert("!23");

         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $(".woPaging").html(data.html_wo_paginator);

       }

     }

   });
 }
 ///////////////////////////////////////////////

 $('#modal-company').on('hidden.bs.modal', function () {
   if($("#issavechanged").val()=="-1" && $("#id_summaryofIssue").val()=="" ){
   swal({
        title: "حذف دستور کار بدون موضوع",
        text: $("#id_summaryofIssue").val(),
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "بلی",
        cancelButtonText: "خیر",
        closeOnConfirm: true
    }, function () {
        cancelform();

    });
  }
   // do something…
 });






 $("#woGroup").change(function(){
   console.log($("#woGroup").val());
   filterWoGroup($("#woGroup").val());
 });
 var saveWoEmForm= function () {
    var form = $(this);
    $.ajax({

      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
          // alert("!23");
         $("#modal-woEM").modal("hide");
         // $("tr").on("click", showAssetDetails);

         // console.log(data.html_asset_list);
        }
        else {

          $("#company-table tbody").html(data.html_asset_list);
          $("#modal-assetcategory .modal-content").html(data.html_asset_form);
        }
      }
    });
   return false;
  };


// $(".js-create-wo").unbind();z
$(".js-create-wo").click(loadForm);
$(".js-bulk-formset-delete-wo").click(LoadFormsetDelete);
$(".js-bulkem-selector").click(LoadFormSetEm);
$("#modal-company").on("submit", ".js-wo-create-form", saveForm);
// $("#modal-company").on("click", ".btn-default", cancelform);
// $('#modal-company').on('hidden.bs.modal',cancelform);
// Update book
$("#company-table").on("click", ".js-update-wo", myWoLoader);
$("#modal-company").on("submit", ".js-wo-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-wo2", loadForm);

$("#modal-company").on("submit", ".js-wo2-delete-form", saveForm);
$("#modal-company").on("submit", ".js-formset-delete-form", saveFormsetForm);
$("#modal-woEm").on("submit", ".js-bulkem-selector-form2", saveWoEmForm);
$(".wo-filter").on("click",filter);

$(document).ready(function(){


  var cururl=window.location.pathname;
  if(cururl.indexOf('details')>-1)
  {

    url_parts=cururl.split('/');
    var test = $('<button/>',
      {
          text: 'Test',
          'data-url':'/WorkOrder/'+url_parts[2]+'/update/',
          click: function () {  },

      });
    // var btn={'data-url':'/WorkOrder/10/update/'};
     $.when(loadForm(test)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad,initWoPertLoad);
  }
});

//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
