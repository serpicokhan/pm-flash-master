// var assetLifeOfflineFrom;
// var assetLifeOnlineFrom;
$(function () {

  var LoadAssetSelector=function(){
    var btn=$(this)
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-company").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        $("#modal-company .modal-content").html(data.form_asset_selector);



       // console.log(elem);
        //console.log("yeyeyey");

      }
    });


  }
  var cancelForm=function(){

    $.ajax({
      url: '/Asset/'+$("#lastAssetid").val()+'/Cancel/',

      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_asset_list);
          $("tr").on("click", showAssetDetails);

          // $("#modal-taskGroup").modal("hide");
         // console.log(data.html_taskGroup_list);
        }
        else {

          $("#company-table tbody").html(data.html_asset_list);
          $("#modal-company .modal-content").html(data.html_asset_form);
        }
      }
    });
    return false;


  };

  var loadForm =function (btn1) {
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

        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_asset_form);
        // var qrcode = new QRCode(document.getElementById("qrcode"), {
        //   width : 100,
        //   height : 100
        // });

        // function makeCode () {
        //   var elText = document.getElementById("id_assetName");
        //
        //   if (!elText.value) {
        //     alert("Input a text");
        //     elText.focus();
        //     return;
        //   }
        //
        //   qrcode.makeCode(elText.value);
        // }
        //
        // makeCode();

        // $("#id_assetName").
        //   on("blur", function () {
        //     makeCode();
        //   }).
        //   on("keydown", function (e) {
        //     if (e.keyCode == 13) {
        //       makeCode();
        //     }
        //   });
        var elem = document.querySelector('.js-switch');
        var init = new Switchery(elem);
        $("#id_assetStatus").change(function(x){
          // console.log("start");
          // console.log(x.cancelable);
          // console.log(x);
          // console.log("end");
          if(x.cancelable)
          js_switch_change();



        });
          $('.selectpicker').selectpicker();
            $("tr").on("click", showAssetDetails);

      }
    });



};
  var LoadFormAssetSelector =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);


    return $.ajax({
      url: $(this).attr("date-url")+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");
        // alert(1);
        $("#modal-assetcategory .modal-content").html(data.modalassetcat);


      }
    });



};

//////////
////////////////Search buttom click#############################
var searchAsset= function (searchStr) {

  searchStr=searchStr.replace(' ','__');
   $.ajax({
     url: $(location).attr('pathname')+searchStr+'/Search/',

     type: 'GET',
     dataType: 'json',
     beforeSend:function(){
       console.log($(location).attr('pathname')+searchStr+'/Search/');
     },
     success: function (data) {

       if (data.form_is_valid) {

         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();

         $("#tbody_company").html(data.html_asset_search_tag_list);
         $(".assetPaging").html(data.html_asset_paginator);

         $("#modal-company").modal("hide");
         $("tr").on("click", showAssetDetails);
        // console.log(data.html_amar_list);
       }
       else {


       }
     },
     error: function (jqXHR, exception,err) {
       // alert(exception);
       console.log(err,jqXHR)
     }
   });
   return false;

 };
///////////
/////////////////////////////

$('#assetSearch').keyup(function(){
searchStr=$("#assetSearch").val();
if(searchStr.trim().length>0){
  if($(location).attr('pathname').split('/').length>3){
      searchAsset(searchStr);
    }
  else {
    searchAsset('0/'+searchStr);



  }
}
else {
  if($(location).attr('pathname').split('/').length>3){
    searchAsset('empty');

  }
  else {
    searchAsset('0/empty');
  }


}
});
////////////////////////////////////////////////////////////////

var js_switch_change=function()
{
  $.ajax({
    url: '/AssetLife/'+$("#lastAssetid").val()+'/eval/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-assetLife").modal({backdrop: 'static', keyboard: false});
      // $('#modal-assetLife').data('bs.modal').options.backdrop = 'static';
    },
    success: function (data) {



      tab="tab-assetlife"

       $('.nav-tabs a[href="#' + tab + '"]').tab('show');

      $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
      // if($("#id_assetStatus").is(":checked")==true)
      // {
      //   $('.nav-tabs a[href="#' + 'tab-correct' + '"]').tab('show');
      // }
      // else {
      //   $('.nav-tabs a[href="#' + 'tab-failur' + '"]').tab('show');
      // }

      $('#id_assetOfflineFrom').pDatepicker({
                              format: 'YYYY/MM/DD',

            autoClose: true,
            onSelect:function(unix){
              assetOfflineFrom=new Date(unix);
            }
          });
      $('#id_assetOnlineFrom').pDatepicker({
                                  format: 'YYYY/MM/DD',

                autoClose: true,
                onSelect: function(unix){

                 // var date1 = new Date(Date.parse($("#id_assetOfflineFrom").attr("value")));
                  // var date2 = new Date(Date.parse($("#id_assetOnlineFrom").attr("value")));
                  assetLifeOnlineFrom=new Date(unix);
                  // var timeDiff = Math.abs(assetLifeOnlineFrom.getTime() - assetLifeOfflineFrom.getTime());
                  // var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                  // alert(diffDays);
                }
                                            });
                                            $('.woselector').autoComplete({
                                              resolver: 'custom',
                                              minLength:1,
                                              formatResult: function (item) {
                                                return {
                                                  value: item.id,
                                                  text: "[" + item.id + "] " + item.summaryofIssue,

                                                };
                                              },
                                              events: {
                                                search: function (qry, callback) {
                                                  // let's do a custom ajax call
                                                  $.ajax(
                                                    '/WorkOrder/GetWos',
                                                    {
                                                      data: { 'qry': qry}
                                                    }
                                                  ).done(function (res) {
                                                    console.log(res);
                                                    callback(res)
                                                  });
                                                },

                                              }
                                            });
                                            $('.woselector').on('autocomplete.select', function (evt, item) {
                                              $("#id_assetWOAssoc").val(item.id);
                                              $('#id_assetWOAssoc').val(item.id).trigger('change');
                                              // $('.basicAutoCompleteCustom').html('');
                                            });





      if($("#id_assetStatus").is(":checked")==true)
      {
        $('.nav-tabs a[href="#' + 'tab-correct' + '"]').tab('show');
      }
      else {
        $('.nav-tabs a[href="#' + 'tab-failur' + '"]').tab('show');
      }
      //console.log(data.html_assetLife_form)
    },
    error:function(x,y,z)
    {
      // alert("123");
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
         $("#tbody_company").html(data.html_asset_list);
         $("#modal-company").modal("hide");
           $("tr").on("click", showAssetDetails);
        // console.log(data.html_asset_list);
       }
       else {

         $("#company-table tbody").html(data.html_asset_list);
         $("#modal-company .modal-content").html(data.html_asset_form);
       }
     }
   });
   return false;
 };
var saveAssetCatForm= function () {
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
         $("#tbody_company").html(data.html_asset_list);
         // alert("!23");
        $("#modal-assetcategory").modal("hide");
        $("tr").on("click", showAssetDetails);

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
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_assetMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_assetMeter").empty();
         $("#tbody_assetMeter").html(data.html_assetMeter_list);
         $("#modal-assetMeter").modal("hide");
         //console.log(data.html_wo_list);
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
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_assetEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_assetEvent").empty();
         $("#tbody_assetEvent").html(data.html_assetEvent_list);
         $("#modal-assetEvent").modal("hide");
         //console.log(data.html_wo_list);
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
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_assetUser").empty();
         $("#tbody_assetUser").html(data.html_assetUser_list);
         $("#modal-assetUser").modal("hide");
         //console.log(data.html_wo_list);
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
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_assetFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_assetFile").empty();
         $("#tbody_assetFile").html(data.html_assetFile_list);
         $("#modal-assetFile").modal("hide");
         //console.log(data.html_wo_list);
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
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_assetWaranty_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_assetWaranty").empty();
          $("#tbody_assetWaranty").html(data.html_assetWaranty_list);
          $("#modal-assetWaranty").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetWaranty-table tbody").html(data.html_assetWaranty_list);
          $("#modal-assetWaranty .modal-content").html(data.html_assetWaranty_form);
        }
      }
    });
  return false;
  };

  var initAssetBusinessLoad=function(){

    $.ajax({

      url: '/AssetBusiness/'+$("#lastAssetid").val()+'/listAssetBusiness',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_assetBusiness_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_assetBusiness").empty();
          $("#tbody_assetBusiness").html(data.html_assetBusiness_list);
          $("#modal-assetBusiness").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetBusiness-table tbody").html(data.html_assetBusiness_list);
          $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
        }
      }
    });
  return false;
  };


    var initAssetPurchaseLoad=function(){

      $.ajax({

        url: '/AssetPurchase/'+$("#lastAssetid").val()+'/listAssetPurchase',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_assetPurchase_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_assetPurchase").empty();
            $("#tbody_assetPurchase").html(data.html_assetPurchase_list);
            $("#modal-assetPurchase").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#assetPurchase-table tbody").html(data.html_assetPurchase_list);
            $("#modal-assetPurchase .modal-content").html(data.html_assetPurchase_form);
          }
        }
      });
    return false;
    };


    var initAssetLifeLoad=function(){

      $.ajax({

        url: '/AssetLife/'+$("#lastAssetid").val()+'/listAssetLife',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_assetLife_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_assetLife").empty();
            $("#tbody_assetLife").html(data.html_assetLife_list);
            $("#modal-assetLife").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#assetLife-table tbody").html(data.html_assetLife_list);
            $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
          }
        }
      });
    return false;
    };



 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initAssetPartLoad,initAssetMeterLoad,initAssetEventLoad,initAssetUserLoad,initAssetFileLoad,initAssetWarantyLoad,initAssetBusinessLoad,initAssetPurchaseLoad,initAssetLifeLoad);
   //,initAssetLifeLoad
   //loadForm(btn);

   //initLoad();
 }
var showAssetSelector=function(){



     $.ajax({
      url: '/Asset/Category/',
      beforeSend: function () {

        $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        //data.modalassetcat
         $("#modal-assetcategory .modal-content").html(data.modalassetcat);
      }
    });


}
var showAssetTypeSelector=function(){
  

  matches=[];
  $(".selection-box:checked").each(function() {
      matches.push(this.value);
  });
  console.log(matches);
     $.ajax({
      url: '/Asset/Types/'+matches,
      beforeSend: function () {

        $("#modal-assettype").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {

        //data.modalassetcat
         $("#modal-assettype .modal-content").html(data.html_asset_type);
      }
    });


}
var showAssetDetails=function()
{
  $(".detail").show();
  $("#p_assetdetails").html($(this).find("td:eq(2)").text());
  showMTTR($(this).attr('date-url'));
  showMTBF($(this).attr('date-url'));
  showAssetWoStatus($(this).attr('date-url'));
  loadAssetOfflineStatus($(this).attr('date-url'));
  // console.log($(this).attr('date-url'));
}
var showMTTR=function(id)
{
  $.ajax({
   url: '/Asset/'+id+'/MTTR/',
   beforeSend: function () {

     // $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});
   },
   success: function (data) {
     // console.log(data);

     //data.modalassetcat
      $(".mttr").html((data.asset_mttr!=null)?data.asset_mttr:'0');
   }
 });
}
var showMTBF=function(id)
{
  $.ajax({
   url: '/Asset/'+id+'/MTBF/',
   beforeSend: function () {

     // $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});
   },
   success: function (data) {
     // console.log(data);

     //data.modalassetcat
      $(".mtbf").html((data.asset_mtbf!=null)?data.asset_mtbf:'0');
   }
 });
}
var showAssetWoStatus=function(id)
{
  urlStr='';

  $.ajax({
   url: '/Asset/'+id+'/WOStatus/',
   beforeSend: function () {

     // $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});
   },
   success: function (data) {
     // console.log(data);

     //data.modalassetcat
      $(".overdue").html((data.asset_overdue!=null)?data.asset_overdue:'0');
      $(".openwo").html((data.asset_openwo!=null)?data.asset_openwo:'0');
      $(".wait4part").html((data.asset_wait4part!=null)?data.asset_wait4part:'0');
   }
 });

}
////////////////////////////////
var loadAssetOfflineStatus=function(id)
{
  $.ajax({
    url: '/Asset/'+id+'/GetAssetOfflineStatus/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
   console.log(data);

    DrawDonat2(data.html_assetOfflineStatus_list,'assetOfflinePie');
    DrawLine(data.html_assetOfflineStatus_list,'assetOfflineLine');
    // alert(data.html_assetOfflineStatus_list.lastbreak);
    $(".lastbreak").html(data.html_assetOfflineStatus_list.lastbreak);
    $("#vertical-timeline").html(data.html_assetOffline_recent);
    // $('#onDemWoComOnTimedh4').text(data.html_dashwoCompleted_list.woCompletedOnTimeNum);
    // $('#onDemWoComh4').text(data.html_dashwoCompleted_list.woCompletedNum);
  }
});
}
function DrawDonat2(data,element)
{


  var doughnutData =
  {

        labels: data.woCompletedAssetId,
        datasets: [
          {
            label: "علل خرابی",
            backgroundColor: ["#3d5a80", "#98c1d9","#e0fbfc","#ee6c4d","#293241"],
            data:data.woCompletedNum,
          }
        ]
      };

  var doughnutOptions = {

      title: {
        display: true,
        text: ''
      },
      legend: {
        display: true,
        position: 'right'
    },

  };

  $('#'+element).remove(); // this is my <canvas> element
  $('#'+element+'-container').append('<canvas id="'+element+'" ></canvas>');
  var ctx = document.getElementById(element).getContext("2d");
  // ctx.clearRect(0, 0, element.width, element.height);



    var myNewChart = new Chart(ctx, {
      type: 'doughnut',
      data: doughnutData,
      options: doughnutOptions
  });

  //var myNewChart = new Chart(ctx).Doughnut(doughnutData, doughnutOptions);

}
function DrawLine(data,element)
{

  var mydate2=[0,0,0,0,0,0,0];
  for(x in data.lineminthname)
  {
    mydate2[data.lineminthname[x]-1]=data.lineAssetofflinecount[x];
  }
  var lineData =
  {

          labels:  ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر","آبان","آذز","دی","بهمن","اسفند"],
        datasets: [
          {
            label: "علل خرابی",
            backgroundColor: ["#3d5a80", "#98c1d9","#e0fbfc","#ee6c4d","#293241"],
            data:mydate2,
          }
        ]
      };

  var lineOptions = {

      title: {
        display: true,
        text: ''
      },
      legend: {
        display: false,
        position: 'right'
    },
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
    }

  };

  $('#'+element).remove(); // this is my <canvas> element
  $('#'+element+'-container').append('<canvas id="'+element+'"></canvas>');
  var ctx = document.getElementById(element).getContext("2d");
  // ctx.clearRect(0, 0, element.width, element.height);


    var myNewChart = new Chart(ctx, {
      type: 'line',
      data: lineData,
      options: lineOptions
  });

  //var myNewChart = new Chart(ctx).Doughnut(doughnutData, doughnutOptions);

}
/////////////////////////////////////
var change_type=function(){
  var myurl=$(this).attr("data-url");
  $.ajax({
    url: myurl,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      $("#modal-assettype").modal("hide");
      if(data.is_valid)
      {
        toastr.success("نوع دارایی با موفقیت به روز شد");
      }
      else
      {
        toastr.error("خطا در بروز رسانی نوع دارایی");
      }

  }
});


}
//for tr click
$("tr").on("click", showAssetDetails);

$("#modal-company").on("click", "#id_asseccategorytxt", showAssetSelector);
//
$(".js-select-asset-type").click(LoadAssetSelector);
$(".js-create-asset").click(myWoLoader);

$("#modal-company").on("submit", ".js-asset-create-form", saveForm);

$("#modal-assetcategory").on("submit", ".js-bulkasset-selector-form2", saveAssetCatForm);

// Update book
$("#company-table ").on("click", ".js-update-asset", myWoLoader);
$("#modal-company").on("submit", ".js-asset-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-asset", loadForm);
$("#modal-company").on("submit", ".js-asset-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
$(".js-bulkasset-category-selector").click(LoadFormAssetSelector);
$(".js-bulkasset-type-selector").click(showAssetTypeSelector);
$("#modal-assettype").on("click", ".asset_type_change", change_type);

});
