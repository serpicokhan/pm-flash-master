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
initWoProblemLoad();
initWoCauseLoad();
initWoActionLoad();
initOfflineStatusLoad();
initEquipCostLoad();
initUserGroupLoad();
initWoStopLoad();
initWoPertLoad();
});
