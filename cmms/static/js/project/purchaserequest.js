
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
        // $("#modal-purchaseRequest").html('');

        $("#modal-purchaseRequest").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-purchaseRequest .modal-content").html(data.html_purchaseRequest_form);
        $('.selectpicker').selectpicker();


        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          minChars:1,
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.partCode + "] " + item.partName,

            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/WoPart/GetParts',
                {
                  data: { 'qry': qry}
                }
              ).done(function (res) {
                callback(res)
              });
            },

          }
        });
        $('.advanced2AutoComplete').on('autocomplete.select', function (evt, item) {
          $("#id_PurchaseRequestPartName").val(item.id);
          $('#id_PurchaseRequestPartName').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });


        $('#id_PurchaseRequestDateTo').pDatepicker({
          format: 'YYYY-MM-DD',
          initialValueType: 'gregorian',
          autoClose:true


      });
        $('#id_PurchaseRequestDateFrom').pDatepicker({
          format: 'YYYY-MM-DD',
          initialValueType: 'gregorian',
          autoClose:true


      });


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
        toastr.success("درخواست با موفقیت ذخیره شد");
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
var loadRelatedAsset=function(){
  asset_id=$("#id_PurchaseRequestAssetMakan").val();
  if(asset_id)
  {
    $.ajax({

      url: '/Asset/'+asset_id+'/listRelatedAsset',
      error:function(x,y,z){
        // console.log(x,y,z)

      },


      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {

          $("#id_PurchaseRequestAsset").empty();
          $("#id_PurchaseRequestAsset").html(data.pval);

          // $("#id_PurchaseRequestAsset").selectpicker();
            $('#id_PurchaseRequestAsset').selectpicker('refresh');

        }
        else {


        }
      }
    });
 return false;
  };

}
var filter=function(){
  // alert("!23");
  window.location.replace("/PurchaseRequest/filter/"+"?q="+$("#p-status").val());
}


$("#p-status").on("change",filter);
$(".js-create-purchaseRequest").click(myprLoader);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-create-form", saveForm);

// Update book
$("#purchaseRequest-table").on("click", ".js-update-purchaseRequest", myprLoader);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-update-form", saveForm);
$("#modal-purchaseRequest").on("change", "#id_PurchaseRequestAssetMakan",loadRelatedAsset);
// Delete book
$("#purchaseRequest-table").on("click", ".js-delete-purchaseRequest", loadForm);
$("#modal-purchaseRequest").on("submit", ".js-purchaseRequest-delete-form", saveForm);
// $('#modal-purchaseRequest').on('hidden.bs.modal',cancelForm);
//$("#purchaseRequest-table").on("click", ".js-update-wo", initxLoad);
});
