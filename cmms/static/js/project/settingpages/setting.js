$(function () {
var initWoProblemLoad=function(){

  $.ajax({

    url: '/SettingPage/WOProblem/listWoProblem',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woProblem_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_woProblem").empty();
        $("#tbody_woProblem").html(data.html_woProblem_list);
        $("#modal-woProblem").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#woProblem-table tbody").html(data.html_woProblem_list);
        $("#modal-woProblem .modal-content").html(data.html_woProblem_form);
      }
    }
  });
return false;
};
var initWoActionLoad=function(){

  $.ajax({

    url: '/SettingPage/WOAction/listWoAction',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woAction_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_woAction").empty();
        $("#tbody_woAction").html(data.html_woAction_list);
        $("#modal-woAction").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#woAction-table tbody").html(data.html_woAction_list);
        $("#modal-woAction .modal-content").html(data.html_woAction_form);
      }
    }
  });
return false;
};
var initEquipCostLoad=function(){

  $.ajax({

    url: '/SettingPage/EquipCost/listEquipCost',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_equipCost_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_equipCost").empty();
        $("#tbody_equipCost").html(data.html_equipCost_list);
        $("#modal-equipCost").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#equipCost-table tbody").html(data.html_equipCost_list);
        $("#modal-equipCost .modal-content").html(data.html_equipCost_form);
      }
    }
  });
return false;
};
var initOfflineStatusLoad=function(){


  $.ajax({

    url: '/SettingPage/OfflineStatus/listOfflineStatus',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_offlineStatus_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_offlineStatus").empty();
        $("#tbody_offlineStatus").html(data.html_offlineStatus_list);
        $("#modal-offlineStatus").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#offlineStatus-table tbody").html(data.html_offlineStatus_list);
        $("#modal-offlineStatus .modal-content").html(data.html_offlineStatus_form);
      }
    }
  });
return false;
};
var initWoCauseLoad=function(){

  $.ajax({

    url: '/SettingPage/WOCause/listWoCause',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_woCause").empty();
        $("#tbody_woCause").html(data.html_woCause_list);
        $("#modal-woCause").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#woCause-table tbody").html(data.html_woCause_list);
        $("#modal-woCause .modal-content").html(data.html_woCause_form);
      }
    }
  });
return false;
};
var initWoStopLoad=function(){

  $.ajax({

    url: '/SettingPage/WOStop/listWoStop',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_woStop").empty();
        $("#tbody_woStop").html(data.html_woStop_list);
        $("#modal-woStop").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#woStop-table tbody").html(data.html_woStop_list);
        $("#modal-woStop .modal-content").html(data.html_woStop_form);
      }
    }
  });
return false;
};
var initWoPertLoad=function(){

  $.ajax({

    url: '/SettingPage/WOPert/listWoPert',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_woPert").empty();
        $("#tbody_woPert").html(data.html_woPert_list);
        $("#modal-woPert").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#woPert-table tbody").html(data.html_woPert_list);
        $("#modal-woPert .modal-content").html(data.html_woPert_form);
      }
    }
  });
return false;
};
var initDashAssetLoad=function(){

  $.ajax({

    url: '/SettingPage/DashAsset/listDashAsset',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_dashAsset").empty();
        $("#tbody_dashAsset").html(data.html_dashAsset_list);

        $("#modal-dashAsset").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#dashAsset-table tbody").html(data.html_woCause_list);
        $("#modal-dashAsset .modal-content").html(data.html_dashAsset_form);
      }
    }
  });
return false;
};
var initUserGroupLoad=function(){

  $.ajax({

    url: '/SettingPage/UserGroup/listUserGroup',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_userGroup").empty();
        $("#tbody_userGroup").html(data.html_userGroup_list);
        $("#modal-userGroup").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        $("#userGroup-table tbody").html(data.html_woCause_list);
        $("#modal-userGroup .modal-content").html(data.html_userGroup_form);
      }
    }
  });
return false;
};
var initMeterCodeLoad=function(){

  $.ajax({

    url: '/SettingPage/MeterCode/listMeterCode',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_meterCode").empty();
        $("#tbody_meterCode").html(data.html_meterCode_list);
        $("#modal-meterCode").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {


      }
    }
  });
return false;
};
var initMiscCostCodeLoad=function(){

  $.ajax({

    url: '/SettingPage/MiscCostCode/listMiscCostCode',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_miscCostCode").empty();
        $("#tbody_miscCostCode").html(data.html_miscCostCode_list);
        $("#modal-miscCostCode").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {


      }
    }
  });
return false;
};
var initKpiException=function(){

  $.ajax({

    url: '/SettingPage/KpiException/listKpiException',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_kpiException").empty();
        $("#tbody_kpiException").html(data.html_kpiException_list);
        $("#modal-kpiException").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {


      }
    }
  });
return false;
};
var initAssetException=function(){

  $.ajax({

    url: '/SettingPage/AssetException/listAssetException',



    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_woCause_list);  // <-- This is just a placeholder for now for testing
        $("#tbody_assetException").empty();
        $("#tbody_assetException").html(data.html_assetException_list);
        $("#modal-assetException").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {


      }
    }
  });
return false;
};
initKpiException();
initWoProblemLoad();
initWoCauseLoad();
initWoActionLoad();
initOfflineStatusLoad();
initEquipCostLoad();
initUserGroupLoad();
initWoStopLoad();
initWoPertLoad();
initDashAssetLoad();
initMeterCodeLoad();
initMiscCostCodeLoad();
initAssetException();
});
