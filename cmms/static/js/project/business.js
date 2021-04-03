
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
        // /$("#modal-business").modal("hide");
        $("#modal-company").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_business_form);

      }
    });



};
var cancelForm=function(){
// alert("!23");
  $.ajax({
    url: '/Business/'+$("#lastBusinessid").val()+'/Cancel/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_business_list);


        // $("#modal-taskGroup").modal("hide");
       // console.log(data.html_taskGroup_list);
      }
      else {

        // $("#company-table tbody").html(data.html_part_list);
        // $("#modal-company .modal-content").html(data.html_part_form);
      }
    }
  });
  return false;


};
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
         $("#tbody_company").html(data.html_business_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_business_list);
       }
       else {

         $("#company-table tbody").html(data.html_business_list);
         $("#modal-company .modal-content").html(data.html_business_form);
       }
     }
   });
   return false;
 };
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

 var initBusinessStockLoad=function(){


   $.ajax({

     url: '/BusinessStock/'+$("#lastBusinessid").val()+'/listBusinessStock',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_businessStock_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_businessStock").empty();
         $("#tbody_businessStock").html(data.html_businessStock_list);
         $("#modal-businessStock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessStock-table tbody").html(data.html_businessStock_list);
         $("#modal-businessStock .modal-content").html(data.html_businessStock_form);
       }
     }
   });
return false;
 };
 var initBusinessMeterLoad=function(){

   $.ajax({

     url: '/BusinessMeter/'+$("#lastBusinessid").val()+'/listBusinessMeter',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_businessMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_businessMeter").empty();
         $("#tbody_businessMeter").html(data.html_businessMeter_list);
         $("#modal-businessMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessMeter-table tbody").html(data.html_businessMeter_list);
         $("#modal-businessMeter .modal-content").html(data.html_businessMeter_form);
       }
     }
   });
return false;
 };


 var initBusinessEventLoad=function(){

   $.ajax({

     url: '/BusinessEvent/'+$("#lastBusinessid").val()+'/listBusinessEvent',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_businessEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_businessEvent").empty();
         $("#tbody_businessEvent").html(data.html_businessEvent_list);
         $("#modal-businessEvent").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessEvent-table tbody").html(data.html_businessEvent_list);
         $("#modal-businessEvent .modal-content").html(data.html_businessEvent_form);
       }
     }
   });
 return false;
 };

 var initBusinessUserLoad=function(){

   $.ajax({

     url: '/BusinessUser/'+$("#lastBusinessid").val()+'/listBusinessUser',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_businessUser").empty();
         $("#tbody_businessUser").html(data.html_businessUser_list);
         $("#modal-businessUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessUser-table tbody").html(data.html_businessUser_list);
         $("#modal-businessUser .modal-content").html(data.html_businessUser_form);
       }
     }
   });
 return false;
 };


 var initBusinessFileLoad=function(){

   $.ajax({

     url: '/BusinessFile/'+$("#lastBusinessid").val()+'/listBusinessFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_businessFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_businessFile").empty();
         $("#tbody_businessFile").html(data.html_businessFile_list);
         $("#modal-businessFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessFile-table tbody").html(data.html_businessFile_list);
         $("#modal-businessFile .modal-content").html(data.html_businessFile_form);
       }
     }
   });
 return false;
 };


  var initBusinessPartLoad=function(){

    $.ajax({

      url: '/BusinessPart/'+$("#lastBusinessid").val()+'/listBusinessPart',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_businessPart_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_businessPart").empty();
          $("#tbody_businessPart").html(data.html_businessPart_list);
          $("#modal-businessPart").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#businessPart-table tbody").html(data.html_businessPart_list);
          $("#modal-businessPart .modal-content").html(data.html_businessPart_form);
        }
      }
    });
  return false;
  };

  var initBusinessAssetLoad=function(){

    $.ajax({

      url: '/BusinessAsset/'+$("#lastBusinessid").val()+'/listBusinessAsset',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_businessBusiness_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_businessAsset").empty();
          $("#tbody_businessAsset").html(data.html_businessAsset_list);
          $("#modal-businessAsset").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#businessAsset-table tbody").html(data.html_businessAsset_list);
          $("#modal-businessAsset .modal-content").html(data.html_businessAsset_form);
        }
      }
    });
  return false;
  };


    var initBusinessPurchaseLoad=function(){

      $.ajax({

        url: '/BusinessPurchase/'+$("#lastBusinessid").val()+'/listBusinessPurchase',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_businessPurchase_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_businessPurchase").empty();
            $("#tbody_businessPurchase").html(data.html_businessPurchase_list);
            $("#modal-businessPurchase").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#businessPurchase-table tbody").html(data.html_businessPurchase_list);
            $("#modal-businessPurchase .modal-content").html(data.html_businessPurchase_form);
          }
        }
      });
    return false;
    };

    var initBusinessLocationLoad=function(){

      $.ajax({

        url: '/BusinessLocation/'+$("#lastBusinessid").val()+'/listBusinessLocation ',

        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_businessLocation_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_businessLocation").empty();
            $("#tbody_businessLocation").html(data.html_businessLocation_list);
            $("#modal-businessLocation").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#businessLocation-table tbody").html(data.html_businessLocation_list);
            $("#modal-businessLocation.modal-content").html(data.html_businessLocation_form);
          }
        }
      });
    return false;
    };



 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoBusinessLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initBusinessFileLoad,initBusinessAssetLoad,initBusinessPartLoad );
   //loadForm(btn);

   //initLoad();
 }



$(".js-create-business").click(myWoLoader);
$("#modal-company").on("submit", ".js-business-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-business", myWoLoader);
$("#modal-company").on("submit", ".js-business-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-business", loadForm);
$("#modal-company").on("submit", ".js-business-delete-form", saveForm);
$('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
