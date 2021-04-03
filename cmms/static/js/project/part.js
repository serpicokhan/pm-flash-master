
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
        // /$("#modal-part").modal("hide");
        $("#modal-company").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_part_form);

      }
    });



};
var cancelForm=function(){

  $.ajax({
    url: '/Part/'+$("#lastPartid").val()+'/Cancel/',

    type: 'post',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_part_list);


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
         $("#tbody_company").html(data.html_part_list);
         $("#modal-company").modal("hide");
         $("tr").on("click", showPartDetails);
         toastr.success("قطعه با موفقیت ثبت گردید");
        // console.log(data.html_part_list);
       }
       else {

         $("#company-table tbody").html(data.html_part_list);
         $("#modal-company .modal-content").html(data.html_part_form);
           toastr.error("خطا در ایجاد قطعه. لطفا ورودیهای خود را کنترل نمایید.");
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

 var initPartStockLoad=function(){



   $.ajax({

     url: '/PartStock/'+$("#lastPartid").val()+'/listPartStock',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_partStock_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_partStock").empty();
         $("#tbody_partStock").html(data.html_partStock_list);
         $("#modal-partStock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partStock-table tbody").html(data.html_partStock_list);
         $("#modal-partStock .modal-content").html(data.html_partStock_form);
       }
     }
   });
return false;
 };
 var initPartMeterLoad=function(){

   $.ajax({

     url: '/PartMeter/'+$("#lastPartid").val()+'/listPartMeter',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_partMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_partMeter").empty();
         $("#tbody_partMeter").html(data.html_partMeter_list);
         $("#modal-partMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partMeter-table tbody").html(data.html_partMeter_list);
         $("#modal-partMeter .modal-content").html(data.html_partMeter_form);
       }
     }
   });
return false;
 };


 var initPartEventLoad=function(){

   $.ajax({

     url: '/PartEvent/'+$("#lastPartid").val()+'/listPartEvent',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_partEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_partEvent").empty();
         $("#tbody_partEvent").html(data.html_partEvent_list);
         $("#modal-partEvent").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partEvent-table tbody").html(data.html_partEvent_list);
         $("#modal-partEvent .modal-content").html(data.html_partEvent_form);
       }
     }
   });
 return false;
 };

 var initPartUserLoad=function(){

   $.ajax({

     url: '/PartUser/'+$("#lastPartid").val()+'/listPartUser',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_partUser").empty();
         $("#tbody_partUser").html(data.html_partUser_list);
         $("#modal-partUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partUser-table tbody").html(data.html_partUser_list);
         $("#modal-partUser .modal-content").html(data.html_partUser_form);
       }
     }
   });
 return false;
 };


 var initPartFileLoad=function(){

   $.ajax({

     url: '/PartFile/'+$("#lastPartid").val()+'/listPartFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_partFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_partFile").empty();
         $("#tbody_partFile").html(data.html_partFile_list);
         $("#modal-partFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#partFile-table tbody").html(data.html_partFile_list);
         $("#modal-partFile .modal-content").html(data.html_partFile_form);
       }
     }
   });
 return false;
 };


  var initPartWarantyLoad=function(){

    $.ajax({

      url: '/PartWaranty/'+$("#lastPartid").val()+'/listPartWaranty',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_partWaranty_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_partWaranty").empty();
          $("#tbody_partWaranty").html(data.html_partWaranty_list);
          $("#modal-partWaranty").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#partWaranty-table tbody").html(data.html_partWaranty_list);
          $("#modal-partWaranty .modal-content").html(data.html_partWaranty_form);
        }
      }
    });
  return false;
  };

  var initPartBusinessLoad=function(){

    $.ajax({

      url: '/PartBusiness/'+$("#lastPartid").val()+'/listPartBusiness',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_partBusiness_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_partBusiness").empty();
          $("#tbody_partBusiness").html(data.html_partBusiness_list);
          $("#modal-partBusiness").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#partBusiness-table tbody").html(data.html_partBusiness_list);
          $("#modal-partBusiness .modal-content").html(data.html_partBusiness_form);
        }
      }
    });
  return false;
  };


    var initPartPurchaseLoad=function(){

      $.ajax({

        url: '/PartPurchase/'+$("#lastPartid").val()+'/listPartPurchase',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_partPurchase_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_partPurchase").empty();
            $("#tbody_partPurchase").html(data.html_partPurchase_list);
            $("#modal-partPurchase").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#partPurchase-table tbody").html(data.html_partPurchase_list);
            $("#modal-partPurchase .modal-content").html(data.html_partPurchase_form);
          }
        }
      });
    return false;
    };

    var initPartLocationLoad=function(){

      $.ajax({

        url: '/PartLocation/'+$("#lastPartid").val()+'/listPartLocation ',

        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_partLocation_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_partLocation").empty();
            $("#tbody_partLocation").html(data.html_partLocation_list);
            $("#modal-partLocation").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#partLocation-table tbody").html(data.html_partLocation_list);
            $("#modal-partLocation.modal-content").html(data.html_partLocation_form);
          }
        }
      });
    return false;
    };



 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initPartStockLoad,initPartLocationLoad,initPartUserLoad,initPartWarantyLoad,initPartBusinessLoad,initPartPurchaseLoad,initPartFileLoad);
   //loadForm(btn);

   //initLoad();
 }
 ////////////////Search buttom click#############################
 var searchPart= function (searchStr) {


    $.ajax({
      url: '/Part/'+searchStr+'/Search/',

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          console.log(data);
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_part_search_tag_list);
          $(".woPaging").html(data.html_part_paginator);
          $("tr").on("click", showPartDetails);
          $("#modal-company").modal("hide");
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
  /////////////////////////////

  $('#partSearch').keyup(function(){

   searchStr=$("#partSearch").val();

   searchStr=searchStr.replace(' ','_');
   // searchStr=searchStr.replace('/\\/','');
   if(searchStr.trim().length>0){
   searchPart(searchStr);
 }
 else {
   searchPart('empty');


 }
    // alert("salam");

 });
 ////////////////////////////////////////////////////////////////
 // var stockpagenume=0;
 // var stockpurchasepagenume=0;
 var showPartDetails=function()
 {
   $(".details").show();
   $("#p_partdetails").html($(this).find("td:eq(0)").text());
   showInventoryLevel($(this).attr('data-url'));
   showInventorySum($(this).attr('data-url'));
   loadPartUsageStatus($(this).attr('data-url'));
   GetConsumeInfo($(this).attr('data-url'));


 }
 var showInventoryLevel=function(id)
 {
   $.ajax({
    url: '/Part/'+id+'/InventoryLevel/',
    beforeSend: function () {

    },
    success: function (data) {

    $("#tbody_inventorylevel").html((data.part_inventory_level!=null)?data.part_inventory_level:'0');
    }
  });
};
 var showInventorySum=function(id)
 {
   $.ajax({
    url: '/Part/'+id+'/InventorySum/',
    beforeSend: function () {

    },
    success: function (data) {
      console.log(data);
    $(".inventory_sum").html((data.part_inventory_sum.qtyOnHand__sum!=null)?data.part_inventory_sum.qtyOnHand__sum:'0');
    }
  });
};
var loadPartUsageStatus=function(id)
{
  $.ajax({
    url: '/Part/'+id+'/GetPartUsage/',
    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
   console.log(data);

    DrawDonat2(data.html_part_maintenance_type_list,'PartPie');
    DrawLine(data.html_part_maintenance_type_list,'PartLine');
    // DrawLine(data.html_part_maintenance_type_list,'assetOfflineLine');
    // alert(data.html_assetOfflineStatus_list.lastbreak);
    // $(".lastbreak").html(data.html_assetOfflineStatus_list.lastbreak);
    // $("#vertical-timeline").html(data.html_assetOffline_recent);
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
            label: "موارد استفاده",
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



  // ctx.clearRect(0, 0, element.width, element.height);


  $('#PartPie').remove(); // this is my <canvas> element
  $('#PartPieHolder').append('<canvas id="PartPie" height="100px"><canvas>');
  var ctx = document.getElementById(element).getContext("2d");
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
  var mydate3=[0,0,0,0,0,0,0,0,0,0,0,0];

  for(x in data.lineminthname)
  {
    mydate2[data.lineminthname[x]-1]=data.lineAssetofflinecount[x];
  }
  for(x in data.linepartpurchasemonth)
  {
    mydate3[data.linepartpurchasemonth[x]-1]=data.linepartpurchasecount[x];
  }


  var lineData =
  {



        labels:  ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر","آبان","آذز","دی","بهمن","اسفند"],
        datasets: [
          {
            label: "مصرف",
            // backgroundColor: "#3d5a80",
            data:mydate2,
            fill:false,
            backgroundColor: "#ee6c4d",
					  borderColor: "#ee6c4d",
          },

          {
          backgroundColor: "#3d5a80",
					borderColor: "#3d5a80",
            label: "خرید",
            // backgroundColor: "#98c1d9",
            data:mydate3,
            fill:false
          }

        ]
      };

  var lineOptions = {

      title: {
        display: true,
        text: ''
      },
      legend: {
        display: true,
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

  $('#PartLine').remove(); // this is my <canvas> element
  $('#PartLineHolder').append('<canvas id="PartLine" height="100px"><canvas>');
  var ctx = document.getElementById(element).getContext("2d");
  // ctx.clearRect(0, 0, element.width, element.height);


    var myNewChart = new Chart(ctx, {
      type: 'line',
      data: lineData,
      options: lineOptions
  });

  //var myNewChart = new Chart(ctx).Doughnut(doughnutData, doughnutOptions);

}
function GetConsumeInfo(id){
  $.ajax({
    url: '/Part/'+id+'/'+0+'/GetConsumes/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // stockpagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing

        $("#vertical_timeline2").html(data.html_stock_list);
        $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
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
  $.ajax({
    url: '/Part/'+id+'/'+0+'/GetPurchases/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // stockpagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing

        $("#vertical_timeline1").html(data.html_stock_list);
        $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
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
}

$("tr").on("click", showPartDetails);
$(".js-create-part").click(myWoLoader);
$("#modal-company").on("submit", ".js-part-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-part", myWoLoader);
$("#modal-company").on("submit", ".js-part-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-part", loadForm);
$("#modal-company").on("submit", ".js-part-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
