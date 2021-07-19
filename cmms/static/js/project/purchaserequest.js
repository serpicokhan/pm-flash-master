
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
         swal({
              title: "درخواست با موفقیت ارسال شد",
              text:"",
              type: "success",

              confirmButtonColor: "#DD6B55",
              confirmButtonText: "تایید",

              closeOnConfirm: true
          }, function () {});
       }
       else {

      
       }
     }
   });
   return false;
 };


 var initPurchaseRequestStockLoad=function(){


   $.ajax({

     url: '/PurchaseRequestStock/'+$("#lastPurchaseRequestid").val()+'/listPurchaseRequestStock',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {

         $("#tbody_purchaseRequestStock").empty();
         $("#tbody_purchaseRequestStock").html(data.html_purchaseRequestStock_list);
         $("#modal-purchaseRequestStock").modal("hide");

       }
       else {

         $("#purchaseRequestStock-table tbody").html(data.html_purchaseRequestStock_list);
         $("#modal-purchaseRequestStock .modal-content").html(data.html_purchaseRequestStock_form);
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
// $('#modal-purchaseRequest').on('hidden.bs.modal',cancelForm);
//$("#purchaseRequest-table").on("click", ".js-update-wo", initxLoad);
});
