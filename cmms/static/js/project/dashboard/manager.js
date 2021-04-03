$(document).ready(function(){
xxxDate1=new persianDate();
dt1=xxxDate1.pDate.year.toString()+"-"+("0" + xxxDate1.pDate.month).slice(-2)+"-01";
$("#dashboardt1").val(dt1);
/////WOPArt
GetWoReqNum();
GetWoPartNum();
GetMTTR();
GetMisc();
GetHighPriorityWO();
GetWoPartNum();
GetStopNum();
GetOverdueWoReqNum();
GetLowItemStock();
GetRequestedWo();
LoadEqCost();


LoadResource(3,"doughnutChartResourceStatus3");
LoadResource(4,"doughnutChartResourceStatus4");
LoadResource(5,"doughnutChartResourceStatus5");
GetEmCount();


/////Donat
// LoadOnDemandDonat();
// LoadPmDonat();
// LoadTotalDonat();

////getResources
// LoadResources();
////
// LoadGroupBar();
// LoadCompletedWorkOrderDonat();
// ///get downtime equpment
// LoadEqDownTime();
// LoadEqCost();
// GetHighPriorityWO();
// GetOpenWoReqNum();
// GetCloseWoReqNum();
// GetOverdueWoReqNum();

});
//date change
$(".btn.btn-white.btn-bitbucket").click(function(){

    //DrawDonat(100,200,'doughnutChartOnDemand');
    GetWoReqNum();
    GetWoPartNum();
    GetMTTR();
    GetMisc();
    GetHighPriorityWO();
    GetWoPartNum();
    GetStopNum();
    GetOverdueWoReqNum();
    GetLowItemStock();
    LoadEqCost();
    LoadResource(3);
    LoadResource(4);
    LoadResource(5);
      LoadCauseBar();
      GetEmCount();


    // GetRequestedWo();


    /////Donat
    // LoadOnDemandDonat();
    // LoadPmDonat();
    // LoadTotalDonat();
    //
    // ////getResources
    // LoadResources();
    // ////
    // LoadGroupBar();
    // LoadCompletedWorkOrderDonat();
    // ///get downtime equpment
    // LoadEqDownTime();
    // GetHighPriorityWO();
    // GetOpenWoReqNum();
    // GetCloseWoReqNum();
    // GetOverdueWoReqNum();
    // LoadEqCost();


});
