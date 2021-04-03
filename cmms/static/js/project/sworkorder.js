
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
            dataType: 'json',
              console.log("hahaha");

            }
          });


        });
        $(".selectpicker").selectpicker();

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


          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
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
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $("#modal-company").modal("hide");
         toastr.success("دستور کار زمانبندی شده با موفقیت  ایجاد شد");

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

    getListWorkorderLastTime(2);
});
//################### ماه #####################
$('#option3').change(function(){

  getListWorkorderLastTime(3);
});

$('#option1').change(function(){

  getListWorkorderLastTime(1);
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
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_task").empty();
         $("#tbody_task").html(data.html_task_list);
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
   $.when(loadForm(btn)).done(initLoad,initWoPartLoad,initialScheduleLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad);
   //loadForm(btn);

   //initLoad();
 }


$(".js-create-swo").click(loadForm);
$("#modal-company").on("submit", ".js-swo-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-swo", myWoLoader);
$("#modal-company").on("submit", ".js-swo-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-swo", loadForm);
$("#modal-company").on("submit", ".js-swo-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelform);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
