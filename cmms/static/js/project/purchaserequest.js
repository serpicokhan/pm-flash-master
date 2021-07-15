
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

        $("#modal-purchaseRequest").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-purchaseRequest .modal-content").html(data.html_purchaseRequest_form);

      }
    });



};
var cancelForm=function(){

  $.ajax({
    url: '/PurchaseRequest/'+$("#lastPurchaseRequestid").val()+'/Cancel/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_purchaseRequest").empty();
        $("#tbody_purchaseRequest").html(data.html_purchaseRequest_list);


        // $("#modal-taskGroup").modal("hide");
       // console.log(data.html_taskGroup_list);
      }
      else {

        // $("#purchaseRequest-table tbody").html(data.html_part_list);
        // $("#modal-purchaseRequest .modal-content").html(data.html_part_form);
      }
    }
  });
  return false;


};
//$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-create-form",
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
         $("#tbody_purchaseRequest").empty();
         $("#tbody_purchaseRequest").html(data.html_purchaseRequest_list);
         $("#modal-purchaseRequest").modal("hide");
        // console.log(data.html_purchaseRequest_list);
       }
       else {

         $("#purchaseRequest-table tbody").html(data.html_purchaseRequest_list);
         $("#modal-purchaseRequest .modal-content").html(data.html_purchaseRequest_form);
       }
     }
   });
   return false;
 };
/*
 $('#modal-purchaseRequest').on('hidden.bs.modal', function () {
   alert("321321");
   console.log($("#lastWorkOrderid").val());
   $.ajax({
     url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/deleteChildren',



     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_purchaseRequest").empty();
         //$("#tbody_purchaseRequest").html(data.html_wo_list);
         //$("#modal-purchaseRequest").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequest-table tbody").html(data.html_wo_list);
         $("#modal-purchaseRequest .modal-content").html(data.html_form);
       }
     }
   });


  // do something…
});
*/
 //alert("321312");
 // Create book

 var initPurchaseRequestStockLoad=function(){


   $.ajax({

     url: '/PurchaseRequestStock/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestStock',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_purchaseRequestStock_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_purchaseRequestStock").empty();
         $("#tbody_purchaseRequestStock").html(data.html_purchaseRequestStock_list);
         $("#modal-purchaseRequestStock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequestStock-table tbody").html(data.html_purchaseRequestStock_list);
         $("#modal-purchaseRequestStock .modal-content").html(data.html_purchaseRequestStock_form);
       }
     }
   });
return false;
 };
 var initPurchaseRequestMeterLoad=function(){

   $.ajax({

     url: '/PurchaseRequestMeter/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestMeter',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_purchaseRequestMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_purchaseRequestMeter").empty();
         $("#tbody_purchaseRequestMeter").html(data.html_purchaseRequestMeter_list);
         $("#modal-purchaseRequestMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequestMeter-table tbody").html(data.html_purchaseRequestMeter_list);
         $("#modal-purchaseRequestMeter .modal-content").html(data.html_purchaseRequestMeter_form);
       }
     }
   });
return false;
 };


 var initPurchaseRequestEventLoad=function(){

   $.ajax({

     url: '/PurchaseRequestEvent/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestEvent',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_purchaseRequestEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_purchaseRequestEvent").empty();
         $("#tbody_purchaseRequestEvent").html(data.html_purchaseRequestEvent_list);
         $("#modal-purchaseRequestEvent").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequestEvent-table tbody").html(data.html_purchaseRequestEvent_list);
         $("#modal-purchaseRequestEvent .modal-content").html(data.html_purchaseRequestEvent_form);
       }
     }
   });
 return false;
 };

 var initPurchaseRequestUserLoad=function(){

   $.ajax({

     url: '/PurchaseRequestUser/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestUser',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_purchaseRequestUser").empty();
         $("#tbody_purchaseRequestUser").html(data.html_purchaseRequestUser_list);
         $("#modal-purchaseRequestUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequestUser-table tbody").html(data.html_purchaseRequestUser_list);
         $("#modal-purchaseRequestUser .modal-content").html(data.html_purchaseRequestUser_form);
       }
     }
   });
 return false;
 };


 var initPurchaseRequestFileLoad=function(){

   $.ajax({

     url: '/PurchaseRequestFile/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_purchaseRequestFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_purchaseRequestFile").empty();
         $("#tbody_purchaseRequestFile").html(data.html_purchaseRequestFile_list);
         $("#modal-purchaseRequestFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#purchaseRequestFile-table tbody").html(data.html_purchaseRequestFile_list);
         $("#modal-purchaseRequestFile .modal-content").html(data.html_purchaseRequestFile_form);
       }
     }
   });
 return false;
 };


  var initPurchaseRequestPartLoad=function(){

    $.ajax({

      url: '/PurchaseRequestPart/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestPart',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_purchaseRequestPart_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_purchaseRequestPart").empty();
          $("#tbody_purchaseRequestPart").html(data.html_purchaseRequestPart_list);
          $("#modal-purchaseRequestPart").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#purchaseRequestPart-table tbody").html(data.html_purchaseRequestPart_list);
          $("#modal-purchaseRequestPart .modal-content").html(data.html_purchaseRequestPart_form);
        }
      }
    });
  return false;
  };

  var initPurchaseRequestAssetLoad=function(){

    $.ajax({

      url: '/PurchaseRequestAsset/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestAsset',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_purchaseRequestPurchaseRequest_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_purchaseRequestAsset").empty();
          $("#tbody_purchaseRequestAsset").html(data.html_purchaseRequestAsset_list);
          $("#modal-purchaseRequestAsset").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#purchaseRequestAsset-table tbody").html(data.html_purchaseRequestAsset_list);
          $("#modal-purchaseRequestAsset .modal-content").html(data.html_purchaseRequestAsset_form);
        }
      }
    });
  return false;
  };


    var initPurchaseRequestPurchaseLoad=function(){

      $.ajax({

        url: '/PurchaseRequestPurchase/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestPurchase',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_purchaseRequestPurchase_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_purchaseRequestPurchase").empty();
            $("#tbody_purchaseRequestPurchase").html(data.html_purchaseRequestPurchase_list);
            $("#modal-purchaseRequestPurchase").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#purchaseRequestPurchase-table tbody").html(data.html_purchaseRequestPurchase_list);
            $("#modal-purchaseRequestPurchase .modal-content").html(data.html_purchaseRequestPurchase_form);
          }
        }
      });
    return false;
    };

    var initPurchaseRequestLocationLoad=function(){

      $.ajax({

        url: '/PurchaseRequestLocation/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestLocation ',

        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_purchaseRequestLocation_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_purchaseRequestLocation").empty();
            $("#tbody_purchaseRequestLocation").html(data.html_purchaseRequestLocation_list);
            $("#modal-purchaseRequestLocation").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#purchaseRequestLocation-table tbody").html(data.html_purchaseRequestLocation_list);
            $("#modal-purchaseRequestLocation.modal-content").html(data.html_purchaseRequestLocation_form);
          }
        }
      });
    return false;
    };



 var myprLoader= function(){
   btn=$(this);




   //$.when(loadForm(btn)).done(initLoad,initWoPurchaseRequestLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   // $.when(loadForm(btn)).done(initPurchaseRequestFileLoad,initPurchaseRequestAssetLoad,initPurchaseRequestPartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-purchaseRequest").click(myprLoader);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-create-form", saveForm);

// Update book
$("#purchaseRequest-table").on("click", ".js-update-purchaseRequest", myprLoader);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-update-form", saveForm);
// Delete book
$("#purchaseRequest-table").on("click", ".js-delete-purchaseRequest", loadForm);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-delete-form", saveForm);
$('#modal-purchaseRequest').on('hidden.bs.modal',cancelForm);
//$("#purchaseRequest-table").on("click", ".js-update-wo", initxLoad);
});
