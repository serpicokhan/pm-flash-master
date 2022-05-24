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

          // $("#tbody_company").empty();
          // $("#tbody_company").html(data.html_asset_list);
          // $("tr").on("click", showAssetDetails);

          // $("#modal-taskGroup").modal("hide");
         // console.log(data.html_taskGroup_list);
         swal("حذف شد!", $("#id_summaryofIssue").val(), "success");
        }
        else {

          $("#company-table tbody").html(data.html_asset_list);
          $("#modal-company .modal-content").html(data.html_asset_form);
        }
      }
    });
    return false;


  };
  $('#modal-company').on('click','.assetclose', function () {
    if($("#issavechanged").val()=="-1" && ($("#id_asseccategorytxt").val()=="" || $("#id_assetName").val().length==0 || $("#id_assetCode").val().length==0) ){
    swal({
         title:"حذف تجهیز بدون کد و مشخصات",
         text: $("#id_summaryofIssue").val(),
         type: "warning",
         showCancelButton: true,
         confirmButtonColor: "#DD6B55",
         confirmButtonText: "بلی",
         cancelButtonText: "خیر",
         closeOnConfirm: true
     }, function () {
         cancelForm();

     });
   }
    // do something…
  });

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
        $("#modal-company .modal-content").html('');

        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_asset_form);
        $('.advanced2AutoComplete3').autoComplete({
          resolver: 'custom',
          noResultsText:'بدون نتیجه',
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.assetCode + "] " + item.assetName,
            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/Asset/GetAssets',
                {
                  data: { 'qry': qry}
                }
              ).done(function (res) {
                callback(res);
              });
            },
          }
        });
        $('.advanced2AutoComplete3').on('autocomplete.select', function (evt, item) {
          // alert("!23");
          $("#id_assetIsPartOf").val(item.id);
        });

//           new QRCode(document.getElementById("qrcode"), {
//     text: data.id,
//     width: 128,
//     height: 128,
//     colorDark : "#000000",
//     colorLight : "#ffffff",
//     correctLevel : QRCode.CorrectLevel.H
// });
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
            // $("tr").on("click", showAssetDetails);




      }
    });



};
  var LoadFormAssetSelector =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    return $.ajax({
      url: $(this).attr("date-url")+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-assetcategory2").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetcategory2 .modal-content").html(data.modalassetcat);
      }
    });



};
  var clone_asset =function () {


    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    return $.ajax({
      url: '/Asset/Clone/'+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        if(data.form_is_valid)
        {
        $("#tbody_company").html(data.html_asset_list);
        $(".assetPaging").html(data.html_asset_paginator);
        // $("tr").on("click", showAssetDetails);
        toastr.success("کپی با موفقیت انجام شد")
      }
      else
      {
        toastr.error("خطا در کپی دارایی");
      }
    }
    });



};
  var duplicate_asset =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    if(matches.length==0)
      return false;
    return $.ajax({
      url: '/Asset/duplicate/'+matches[0],
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
          $("#modal-assetcategory2").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
          $("#modal-assetcategory2 .modal-content").html(data.modalassetcat);
      }
    });
};
var bulk_delete_pressed=function(){
  swal({
       title:"حذف تجهیز بدون کد و مشخصات",
       text: $("#id_summaryofIssue").val(),
       type: "warning",
       showCancelButton: true,
       confirmButtonColor: "#DD6B55",
       confirmButtonText: "بلی",
       cancelButtonText: "خیر",
       closeOnConfirm: true
   }, function () {
       bulk_delete_asset();

   });
}
  var bulk_delete_asset =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);


    return $.ajax({
      url: '/Asset/BulkDelete/'+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {



      },
      success: function (data) {
        if(data.form_is_valid)
        {
        $("#tbody_company").html(data.html_asset_list);
        $(".assetPaging").html(data.html_asset_paginator);


        // $("tr").on("click", showAssetDetails);
        swal("حذف شد!",'', "success");
      }
      else
      {
        toastr.error("خطا در حذف دسته ای دارایی ها");
      }
    }
    });
};
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}
//////////
////////////////Search buttom click#############################
var searchAsset= function (loc,searchStr) {
  // searchStr=searchStr.replace(' ','__');
  // console.log('/Asset/'+loc+'/Search/?q='+searchStr);
   $.ajax({
     url: '/Asset/'+loc+'/Search/?q='+searchStr+'&page='+findGetParameter('page'),
     type: 'GET',
     dataType: 'json',
     beforeSend:function(){
       // console.log($(location).attr('pathname')+searchStr+'/Search/');
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_asset_search_tag_list);
         $(".assetPaging").html(data.html_asset_paginator);
         $("#modal-company").modal("hide");
         // $("tr").on("click", showAssetDetails);
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
  loc_path=$(location).attr('pathname').split('/');
  if(loc_path.length>3){
  kvm_=0
  if(loc_path[2]=='Location')
      kvm_='1';
  else if(loc_path[2]='Machine')
    kvm_='2';
  else {
    kvm_='3'
  }

      searchAsset(kvm_,searchStr);
    }
  else {
    searchAsset('0',searchStr);



  }
}
else {

  loc_path=$(location).attr('pathname').split('/');
  if(loc_path.length>3){
    kvm_=0
    if(loc_path.length>3){
    kvm_=0
    if(loc_path[2]=='Location')
        kvm_='1';
    else if(loc_path[2]='Machine')
      kvm_='2';
    else {
      kvm_='3'
    }
    searchAsset(kvm_,'');

  }




}
else {
  searchAsset('0','');
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
            // onSelect:function(unix){
            //   assetOfflineFrom=new Date(unix);
            // }
          });
      $('#id_assetOnlineFrom').pDatepicker({
                                  format: 'YYYY/MM/DD',

                autoClose: true,
                // onSelect: function(unix){
                //
                //  // var date1 = new Date(Date.parse($("#id_assetOfflineFrom").attr("value")));
                //   // var date2 = new Date(Date.parse($("#id_assetOnlineFrom").attr("value")));
                //   assetLifeOnlineFrom=new Date(unix);
                //   // var timeDiff = Math.abs(assetLifeOnlineFrom.getTime() - assetLifeOfflineFrom.getTime());
                //   // var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                //   // alert(diffDays);
                // }
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
     beforeSend:function(x,h)
     {
       if(!$(this)[0].url.includes('delete')){
       if($("#id_assetCategory").val().length==0)
       {
         toastr.error("دسته تجهیز را مشخص کنید");
         x.abort();
       }
     }
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_asset_list);
         $("#modal-company").modal("hide");
           // $("tr").on("click", showAssetDetails);
            $("#issavechanged").val("1");
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
   console.log("it happend>");
   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(){
       // console.log(form.serialize());
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_asset_list);
         // alert("!23");
        $("#modal-assetcategory2").modal("hide");
        // $("tr").on("click", showAssetDetails);

       }
       else {

         toastr.error(data.error);
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
 var initAssetMeterTemplateLoad=function(){

   $.ajax({

     url: '/AssetMeterTemplate/'+$("#lastAssetid").val()+'/listAssetMeterTemplate',



     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_assetAMT").empty();
         $("#tbody_assetAMT").html(data.html_assetMeterTemplate_list);
         $("#modal-assetAMT").modal("hide");
       }
       else {

         $("#assetAMT-table tbody").html(data.html_assetMeterTemplate_list);
         $("#modal-assetAMT .modal-content").html(data.html_assetMeterTemplate_form);
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
    // //////////////////////////////////////
 var myWoLoader= function(){
   btn=$(this);
   $.when(loadForm(btn)).done(initAssetPartLoad,initAssetMeterLoad,initAssetEventLoad,initAssetUserLoad,initAssetFileLoad,initAssetWarantyLoad,initAssetBusinessLoad,initAssetPurchaseLoad,initAssetLifeLoad,initAssetTreeInit,initAssetWoLoad,initAssetCloseWoLoad,initAssetConsumedPartLoad,initAssetSWoLoad,initAssetAssetLoad,initAssetMeterTemplateLoad);
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
  $("#p_assetdetails").html($(this).find("td:eq(1)").text());
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
     // //console.log(data);

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
     // //console.log(data);

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
     // //console.log(data);

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
   // //console.log(data);

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

  var mydate2=[0,0,0,0,0,0,0,0,0,0,0,0];
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
/////////////////////////////////////
$("#assetStatus").change(function(){
  // var myurl=$(this).attr("data-url");
  $.ajax({
    url: '/Asset/'+$("#assetStatus").val()+'/show_Asset_status/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      if (data.form_is_valid) {

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_company").empty();

        $("#tbody_company").html(data.html_asset_search_tag_list);
        $(".assetPaging").html(data.html_asset_paginator);

        $("#modal-company").modal("hide");
        // $("tr").on("click", showAssetDetails);
       // console.log(data.html_amar_list);
      }
      else {


      }

  }
});


});
var gen_code=function(){
  loc=-1;
  if($("#id_assetIsLocatedAt").val()>0)
  {
    loc=$("#id_assetIsLocatedAt").val();
  }
  $.ajax({
    url: '/Asset/'+$("#lastAssetid").val()+'/gen_code?loc='+loc+'&pishvand='+$("#id_assetCode").val(),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      if (data.form_is_valid) {

        //alert("Company created!");  // <-- This is just a placeholder for now for testing
      $("#id_assetCode").val(data.code);
      }
      else {


      }

  }
});
}
//for tr click
$(".js-create-asset").unbind();
// $("tr").on("click", showAssetDetails);

$("#modal-company").on("click", "#id_asseccategorytxt", showAssetSelector);
//
$(".js-select-asset-type").click(LoadAssetSelector);
$(".js-create-asset").click(myWoLoader);

$("#modal-company").on("submit", ".js-asset-create-form", saveForm);

$("#modal-assetcategory2").on("submit", ".js-bulkasset-selector-form2", saveAssetCatForm);
$("#modal-assetcategory2").on("submit", ".js-bulkasset-duplicate-form", saveAssetCatForm);

// Update book
$("#company-table ").on("click", ".js-update-asset", myWoLoader);
$("#modal-company").on("submit", ".js-asset-update-form", saveForm);
$("#modal-company").on("click", ".btn_code_gen", gen_code);
// Delete book
$("#company-table").on("click", ".js-delete-asset", loadForm);
$("#company-table").on("click", "tr", showAssetDetails);
$("#modal-company").on("submit", ".js-asset-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
$(".js-bulkasset-category-selector").click(LoadFormAssetSelector);
$(".js-clone-asset").click(clone_asset);
$(".js-duplicate-asset").click(duplicate_asset);
$(".js-bulk_delete-asset").click(bulk_delete_pressed);
$(".js-bulkasset-type-selector").click(showAssetTypeSelector);
$("#modal-assettype").on("click", ".asset_type_change", change_type);

});
