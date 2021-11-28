
$(function () {
  var chkselection=function(){
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    if(matches.length>0)
    {
    $(".js-create-swo-copy").show();
  }
  else{
    $(".js-create-swo-copy").hide();

  }

  };
  var LoadFormCopySelector =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);


    return $.ajax({
      url: $(this).attr("data-url")+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-copy").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#modal-copy .modal-content").html(data.modalcopyasset);


      }
    });



};

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
        var elem = document.querySelector('.js-switch');
        var init = new Switchery(elem);
        $("#id_running").change(function(){
          $.ajax({
            url: $("#lastWorkOrderid").val()+'/Running/',
            type:'get',

            dataType: 'json',
            success: function (data) {

            }
          });


        });
        $("#id_woAsset").change(function(){
          $.ajax({
            url: $("#lastWorkOrderid").val()+'/'+$("#id_woAsset").val()+'/setAsset/',
            type:'get',
            success: function (data) {
            if(data.form_is_valid){
              toastr.success("تجهیز با موفقیت تغییر پیدا نمود.");
            }
            else
            {
              toastr.error("متاسفانه خطایی رخ داده است");
            }

          },
          error:function(){
            toastr.error("متاسفانه خطایی رخ داده است");
          }
          });


        });
        $(".selectpicker").selectpicker();

        initLoad();
        initWoPartLoad();
        initialScheduleLoad();
        initWoMiscLoad();
        initWoNotifyLoad();
        initWoFileLoad();
        initWoLogLoad();

      }
    });



};
var cancelform=function(){

    return $.ajax({
      url: '/SWorkOrder/'+$("#lastWorkOrderid").val()+'/cancel/',
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
          // $("#tbody_company").empty();
          // $("#tbody_company").html(data.html_wo_list);
         // $("#modal-company").modal("hide");

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
     beforeSend:function(xhr, opts){
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
       if($("#haveschedule").val()=="-1")
       {
         toastr.error("برنامه زمانبندی انتخاب نشده است!");
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
         toastr.success("دستور کار زمانبندی شده با موفقیت  ایجاد شد");
         $("#issavechanged").val("1");

        // console.log(data.html_wo_list);
       }
       else {

         $("#company-table tbody").html(data.html_wo_list);
         $("#modal-company .modal-content").html(data.html_wo_form);
         toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");
       }
     }
   });
   return false;
 };
var saveCopy= function () {
   var form = $(this);

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(xhr, opts){

     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $(".woPaging").html(data.html_swo_paginator);
         $("#modal-copy").modal("hide");


         $("#issavechanged").val("1");

        // console.log(data.html_wo_list);
       }
       else {

         $("#company-table tbody").html(data.html_wo_list);
         $("#modal-company .modal-content").html(data.html_wo_form);
         toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");
       }
     }
   });
   return false;
 };


 //############# Time Change ############################
 var get_swo_by_type= function (n) {




    $.ajax({
      url: '/SWorkOrder/'+n+'/swo_show_swo_by_type/',

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_swo_list);
          $(".woPaging").html(data.html_swo_paginator);

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
  ///////////////////////////////
 var swo_show_swo_by_schedule_type= function (n) {




    $.ajax({
      url: '/SWorkOrder/'+n+'/swo_show_swo_by_schedule_type/',

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_swo_list);
          $(".woPaging").html(data.html_swo_paginator);

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
  ///////////////////////////////
  ////////////////Search buttom click#############################
  var searchSWorkorderByTags= function (searchStr) {

    // if(searchStr.length==0)
    // searchStr='empty_'
    // searchStr=searchStr.replace(' ','_')
     $.ajax({
       url: '/SWorkOrder/'+searchStr+'/Search/',

       type: 'GET',
       dataType: 'json',
       success: function (data) {

         if (data.form_is_valid) {
           // console.log(data);
           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           $("#tbody_company").empty();

           $("#tbody_company").html(data.html_swo_list);
           $(".woPaging").html(data.html_swo_paginator);

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
   /////////////////////////////
   $('#swoSearch').on('input',function(){
     strTag=$("#swoSearch").val();
      if(strTag.length==0)
      strTag='empty_';
      strTag=strTag.replace(' ','_');

      searchSWorkorderByTags(strTag);
     //alert("salam");

  });

  //############# Time Radio Button هفته###################
  $('#option2').change(function(){

    get_swo_by_type(2);
});
//################### ماه #####################
$('#option3').change(function(){

  get_swo_by_type(3);
});

$('#option1').change(function(){

  get_swo_by_type(1);
});
$('#woScheduleGroup').change(function(){
  // alert("!23");

  swo_show_swo_by_schedule_type($('#woScheduleGroup').val());
});
/*
 $('#modal-company').on('hidden.bs.modal', function () {
   alert("321321");
   console.log($("#lastWorkOrderid").val());
   $.ajax({
     url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/deleteChildren',



     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_company").empty();
         //$("#tbody_company").html(data.html_wo_list);
         //$("#modal-company").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#company-table tbody").html(data.html_wo_list);
         $("#modal-company .modal-content").html(data.html_form);
       }
     }
   });


  // do something…
});
*/
 //alert("321312");
 // Create book
 var initLoad=function()
 {
   //alert("initload");
   $.ajax({

     url: '/Task/'+$("#lastWorkOrderid").val()+'/listTask',



     success: function (data) {
       // console.log(data);
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_task").empty();
         console.log(data);
         $("#tbody_task").html(data.html_task_list);
         // console.log(data);

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
 var initialScheduleLoad=function(){

   $.ajax({

     url: '/Schedule/'+$("#lastWorkOrderid").val()+'/listSchedule',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_schedule").empty();
         $("#tbody_schedule").html(data.html_schedule_list);
         if(data.is_not_empty)
         {
           $("#haveschedule").val("1");

         }
         // console.log(data.html_schedule_list);
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
 var myWoLoader= function(){

   btn=$(this);
   //console.log(btn);

   loadForm(btn);

   //initLoad();
 }

 //////////////
 $('#modal-company').on('click','.woclose', function () {
   



   if($("#issavechanged").val()=="-1" && $("#id_summaryofIssue").val()=="" ){
   swal({
        title: "حذف دستور کار بدون موضوع",
        text: $("#id_summaryofIssue").val(),
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "بلی",
        cancelButtonText: "خیر",
        closeOnConfirm: false
    }, function () {
        cancelform();

    });
  }

   // do something…
 });



 /////////////


$(".js-create-swo").click(loadForm);
$(".js-create-swo-copy").click(LoadFormCopySelector);
$("#modal-company").on("submit", ".js-swo-create-form", saveForm);
// $("#modal-copy").on("submit", ".js-swo-create-swo-copy", saveForm);

// Update book
$("#company-table").on("click", ".js-update-swo", myWoLoader);
$("#company-table").on("click", ".selection-box", chkselection);
$("#modal-company").on("submit", ".js-swo-update-form", saveForm);
$("#modal-copy").on("submit", ".js-swo-copy-2", saveCopy);
// Delete book
$("#company-table").on("click", ".js-delete-swo", loadForm);
$("#modal-company").on("submit", ".js-swo-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelform);
//$("#company-table").on("click", ".js-update-wo", initxLoad);


$(document).ready(function(){


  var cururl=window.location.pathname;
  if(cururl.indexOf('details')>-1)
  {

    url_parts=cururl.split('/');
    var test = $('<button/>',
      {
          text: 'Test',
          'data-url':'/SWorkOrder/'+url_parts[2]+'/update/',
          click: function () {  },

      });
    // var btn={'data-url':'/WorkOrder/10/update/'};
     $.when(loadForm(test)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad,initWoPertLoad);
  }
});
});