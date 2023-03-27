$(function () {
  var loadForm =function (btn1) {
    var btn=0;
    // console.log(btn1);
   btn=btn1;

    return $.ajax({
      url: btn.attr("data-url2"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_asset_form);
        $("#assetformupdatesubmit").hide();

        var elem = document.querySelector('.js-switch');
        var init = new Switchery(elem);
        $("#id_assetStatus").change(function(x){

          // if(x.cancelable)
          // js_switch_change();



        });
          $('.selectpicker').selectpicker();
            // $("tr").on("click", showAssetDetails);

      }
    });



};
var initAssetPartLoad=function(){


  $.ajax({

    url: '/AssetPart/'+$("#lastAssetid").val()+'/listAssetPart',



    success: function (data) {

      if (data.form_is_valid) {

        $("#tbody_assetPart").empty();
        $("#tbody_assetPart").html(data.html_assetPart_list);
        $("#modal-assetPart").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#assetPart-table tbody").html(data.html_assetPart_list);
        $("#modal-assetPart .modal-content").html(data.html_assetPart_form);
      }
    }
  });
return false;
};
var initAssetMeterLoad=function(){

  $.ajax({

    url: '/AssetMeter/'+$("#lastAssetid").val()+'/listAssetMeter',



    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetMeter").empty();
        $("#tbody_assetMeter").html(data.html_assetMeter_list);
        $("#modal-assetMeter").modal("hide");
      }
      else {

        $("#assetMeter-table tbody").html(data.html_assetMeter_list);
        $("#modal-assetMeter .modal-content").html(data.html_assetMeter_form);
      }
    }
  });
return false;
};
var initAssetEventLoad=function(){
  $.ajax({
    url: '/AssetEvent/'+$("#lastAssetid").val()+'/listAssetEvent',
    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetEvent").empty();
        $("#tbody_assetEvent").html(data.html_assetEvent_list);
        $("#modal-assetEvent").modal("hide");
      }
      else {

        $("#assetEvent-table tbody").html(data.html_assetEvent_list);
        $("#modal-assetEvent .modal-content").html(data.html_assetEvent_form);
      }
    }
  });
return false;
};
var initAssetUserLoad=function(){
  $.ajax({
    url: '/AssetUser/'+$("#lastAssetid").val()+'/listAssetUser',
    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetUser").empty();
        $("#tbody_assetUser").html(data.html_assetUser_list);
        $("#modal-assetUser").modal("hide");
      }
      else {

        $("#assetUser-table tbody").html(data.html_assetUser_list);
        $("#modal-assetUser .modal-content").html(data.html_assetUser_form);
      }
    }
  });
return false;
};
var initAssetFileLoad=function(){
  $.ajax({
    url: '/AssetFile/'+$("#lastAssetid").val()+'/listAssetFile',
    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetFile").empty();
        $("#tbody_assetFile").html(data.html_assetFile_list);
        $("#modal-assetFile").modal("hide");
      }
      else {

        $("#assetFile-table tbody").html(data.html_assetFile_list);
        $("#modal-assetFile .modal-content").html(data.html_assetFile_form);
      }
    }
  });
return false;
};
 var initAssetWarantyLoad=function(){
   $.ajax({
     url: '/AssetWaranty/'+$("#lastAssetid").val()+'/listAssetWaranty',
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_assetWaranty").empty();
         $("#tbody_assetWaranty").html(data.html_assetWaranty_list);
         $("#modal-assetWaranty").modal("hide");
       }
       else {

         $("#assetWaranty-table tbody").html(data.html_assetWaranty_list);
         $("#modal-assetWaranty .modal-content").html(data.html_assetWaranty_form);
       }
     }
   });
 return false;
 };
 //////////////////////////////
 var initAssetBusinessLoad=function(){
   $.ajax({
     url: '/AssetBusiness/'+$("#lastAssetid").val()+'/listAssetBusiness',
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_assetBusiness").empty();
         $("#tbody_assetBusiness").html(data.html_assetBusiness_list);
         $("#modal-assetBusiness").modal("hide");
       }
       else {

         $("#assetBusiness-table tbody").html(data.html_assetBusiness_list);
         $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
       }
     }
   });
 return false;
 };
 //////////////////////////////
 var initAssetAssetLoad=function(){
   $.ajax({
     url: '/Asset/Asset/'+$("#lastAssetid").val()+'/listAssetAsset',
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_assetAsset").empty();
         $("#tbody_assetAsset").html(data.html_assetAsset_list);
         $("#modal-assetAsset").modal("hide");
         // $('.advanced2AutoComplete2').autoComplete({
         //   resolver: 'custom',
         //   noResultsText:'بدون نتیجه',
         //   formatResult: function (item) {
         //     return {
         //       value: item.id,
         //       text: "[" + item.id + "] " + item.assetName,
         //     };
         //   },
         //   events: {
         //     search: function (qry, callback) {
         //       // let's do a custom ajax call
         //       $.ajax(
         //         '/Asset/GetAssets',
         //         {
         //           data: { 'qry': qry}
         //         }
         //       ).done(function (res) {
         //         console.log(res);
         //         callback(res);
         //       });
         //     },
         //   }
         // });
         // $('.advanced2AutoComplete2').on('autocomplete.select', function (evt, item) {
         //   $("#id_lastassetasset").val(item.id);
         //   console.log($("#id_lastassetasset").val());
         // });
       }
       else {

         $("#assetBusiness-table tbody").html(data.html_assetBusiness_list);
         $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
       }
     }
   });
 return false;
 };
 //////////////////////////////
   var initAssetPurchaseLoad=function(){
     $.ajax({
       url: '/AssetPurchase/'+$("#lastAssetid").val()+'/listAssetPurchase',
       success: function (data) {
         if (data.form_is_valid) {
           $("#tbody_assetPurchase").empty();
           $("#tbody_assetPurchase").html(data.html_assetPurchase_list);
           $("#modal-assetPurchase").modal("hide");
         }
         else {

           $("#assetPurchase-table tbody").html(data.html_assetPurchase_list);
           $("#modal-assetPurchase .modal-content").html(data.html_assetPurchase_form);
         }
       }
     });
   return false;
   };
   ///////////////////////////
   var initAssetLifeLoad=function(){
     $.ajax({
       url: '/AssetLife/'+$("#lastAssetid").val()+'/listAssetLife',
       success: function (data) {
         if (data.form_is_valid) {
           $("#tbody_assetLife").empty();
           $("#tbody_assetLife").html(data.html_assetLife_list);
           $("#modal-assetLife").modal("hide");
         }
         else {
           $("#assetLife-table tbody").html(data.html_assetLife_list);
           $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
         }
       }
     });
   return false;
   };
   ////////////////////////
   var initAssetWoLoad=function(){
     $.ajax({
       url: '/Asset/'+$("#lastAssetid").val()+'/listAssetWO/',
       success: function (data) {
         if (data.form_is_valid) {
           $("#tbody_assetWo").empty();
           $("#tbody_assetWo").html(data.html_assetWo_list);
         }
         else {
         }
       }
     });
   return false;
   };
   var initAssetSWoLoad=function(){
     $.ajax({
       url: '/Asset/'+$("#lastAssetid").val()+'/listAssetSWO/',
       success: function (data) {
         if (data.form_is_valid) {
           $("#tbody_assetSWo").empty();
           $("#tbody_assetSWo").html(data.html_assetSWo_list);
         }
         else {
         }
       }
     });
   return false;
   };
   var initAssetCloseWoLoad=function(){
     $.ajax({
       url: '/Asset/'+$("#lastAssetid").val()+'/listAssetCloseWO/',
       success: function (data) {
         if (data.form_is_valid) {
           $("#tbody_assetCloseWo").empty();
           $("#tbody_assetCloseWo").html(data.html_assetCloseWo_list);
         }
         else {

         }
       }
     });
   return false;
   };
   //////////////////////
   var initAssetConsumedPartLoad=function(){
     $.ajax({
       url: '/Asset/'+$("#lastAssetid").val()+'/listAssetConsumedPart/',
       success: function (data) {
           //alert($("#lastWorkOrderid").val());
         if (data.form_is_valid) {
           $("#tbody_assetCloseWo").empty();
           $("#tbody_assetCloseWo").html(data.html_assetConsumedPart_list);
         }
         else {
         }
       }
     });
   return false;
   };
   var initAssetTreeInit=function(){

     $.ajax({
       url: '/Asset/'+$("#lastAssetid").val()+'/listtree/',
       success: function (data) {
           //alert($("#lastWorkOrderid").val());
         if (data.form_is_valid) {
           $("#htmlmachineasset").html(data.result);
         }
         else {
         }
       }
     });
   return false;
   };
  $(".col-lg-3").on('click',function(){

// loadForm($(this));
// initAssetPartLoad();
 $.when(loadForm($(this))).done(initAssetPartLoad,initAssetMeterLoad,initAssetEventLoad,initAssetUserLoad,initAssetFileLoad,initAssetWarantyLoad,initAssetBusinessLoad,initAssetPurchaseLoad,initAssetLifeLoad,initAssetTreeInit,initAssetWoLoad,initAssetCloseWoLoad,initAssetConsumedPartLoad,initAssetSWoLoad,initAssetAssetLoad);

  });
});
