$(document).ready(function(){
xxxDate1=new persianDate();
dt1=xxxDate1.pDate.year.toString()+"-"+("0" + xxxDate1.pDate.month).slice(-2)+"-01";
$("#dashboardt1").val(dt1);
/////WOPArt
GetWoReqNum();
GetPmpAll();
LoadResources();
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
getDueService();
LoadMTTRBar();
GetPmpLineAll();

for(var i in a111){
  LoadResource(a111[i],"doughnutChartResourceStatus"+a111[i]);
}

// LoadResource(2,"doughnutChartResourceStatus2");
// LoadResource(5,"doughnutChartResourceStatus5");
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
    var ex=$("#makans").val();
    //DrawDonat(100,200,'doughnutChartOnDemand');
    if(ex=='-1')
    {
    GetWoReqNum();
    GetPmpAll();
    LoadResources();
    GetWoPartNum();
    // GetMTTR();
    GetMisc();
    GetHighPriorityWO();
    // GetWoPartNum();
    GetStopNum();
    GetOverdueWoReqNum();
    GetLowItemStock();
    LoadEqCost();
    LoadMTTRBar();
    GetPmpLineAll();
    for ( i=0;i<ggid.length;i++){

    LoadResource(ggid[i],"doughnutChartResourceStatus"+ggid[i]);
  }
    LoadCauseBar();
    GetEmCount();
    getDueService();
  }
  else
  {
    GetPmpAll();
    LoadResources();
    GetWoReqNum2(ex);
    GetWoPartNum2(ex);
    GetMisc2(ex);
    GetHighPriorityWO2(ex);
    LoadEqCost2(ex);
    GetStopNum2(ex);
    GetOverdueWoReqNum2(ex);
    for ( i=0;i<ggid.length;i++){

    LoadResource2(ggid[i],"doughnutChartResourceStatus"+ggid[i],ex);
  }
  LoadCauseBar2(ex);
  GetEmCount2(ex);
  getDueService2(ex);
}
});
$("#makans").change(function(){
  GetPmpAll();
  GetPmpLineAll();
  LoadMTTRBar();

    var ex=$("#makans").val();
    LoadResources();
    //DrawDonat(100,200,'doughnutChartOnDemand');
    if(ex=='-1')
    {
    GetWoReqNum();
    GetWoPartNum();
    // GetMTTR();
    GetMisc();
    GetHighPriorityWO();
    // GetWoPartNum();
    GetStopNum();
    GetOverdueWoReqNum();
    GetLowItemStock();
    LoadEqCost();
    for ( i=0;i<ggid.length;i++){

    LoadResource(ggid[i],"doughnutChartResourceStatus"+ggid[i]);
  }
    LoadCauseBar();
    GetEmCount();
    getDueService();
  }
  else
  {

    GetWoReqNum2(ex);
    GetWoPartNum2(ex);
    GetMisc2(ex);
    GetHighPriorityWO2(ex);
    LoadEqCost2(ex);
    GetStopNum2(ex);
    GetOverdueWoReqNum2(ex);
    for ( i=0;i<ggid.length;i++){

    LoadResource2(ggid[i],"doughnutChartResourceStatus"+ggid[i],ex);
  }
  LoadCauseBar2(ex);
  GetEmCount2(ex);
  getDueService2(ex);
}





});
