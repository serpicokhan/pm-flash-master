var GetWoPartNum= function () {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoPartNum/',
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#monthlyWoPartNumRep").html(data.html_monthlywopartnumrep_list);



     }
   });
   return false;
 };
var GetWoPartNum2= function (loc) {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoPartNum2/'+loc,
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#monthlyWoPartNumRep").html(data.html_monthlywopartnumrep_list);


     }
   });
   return false;
 };
var GetStopNum= function () {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetStopNum/',
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#stopNumRep").html(data.html_stopnumrep_list);



     }
   });
   return false;
 };
var GetStopNum2= function (loc) {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetStopNum2/'+loc,
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#stopNumRep").html(data.html_stopnumrep_list);



     }
   });
   return false;
 };

 ///////////////
 var GetWoReqNum= function () {

    $.ajax({
      url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoReqNum/',
      type:'get',
      dataType: 'json',
      success: function (data) {


          $("#monthlyWoReqNumRep").html(data.html_monthlyworeqnumrep_list);



      }
    });
    return false;
  };
  var GetWoReqNum2= function (loc) {

     $.ajax({
       url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoReqNum2/'+loc,
       type:'get',
       dataType: 'json',
       success: function (data) {


           $("#monthlyWoReqNumRep").html(data.html_monthlyworeqnumrep_list);



       }
     });
     return false;
   };

//////////////////
var GetMTTR= function () {

  $.ajax({
    url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetMTTR/',
    type:'get',
    dataType: 'json',
    success: function (data) {


      $("#monthlyMTTR").html(data.html_monthlymttrrep_list);


    }
  });
  return false;
};

//////////////////
var GetMisc= function () {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetMiscCost/',
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#monthlyMisc").html(data.html_monthlymiscrep_list);

     }
   });
   return false;
 };
var GetMisc2= function (loc) {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetMiscCost2/'+loc,
     type:'get',
     dataType: 'json',
     success: function (data) {


         $("#monthlyMisc").html(data.html_monthlymiscrep_list);


     }
   });
   return false;
 };
///
var GetHighPriorityWO= function () {


   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetHighPriorityWo/',
     type:'get',
     dataType: 'json',
     success: function (data) {



         $("#HighPriorityWO").html(data.html_highprioritywo_list);



     }
   });
   return false;
 };
var GetHighPriorityWO2= function (loc) {


   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetHighPriorityWo2/'+loc,
     type:'get',
     dataType: 'json',
     success: function (data) {



         $("#HighPriorityWO").html(data.html_highprioritywo_list);



     }
   });
   return false;
 };
 ///
 var GetOpenWoReqNum= function () {

    $.ajax({
      url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetOpenWoReqNum/',
      type:'get',
      dataType: 'json',
      success: function (data) {


          $("#openWoReqNumRep").html(data.html_openworeqnumrep_list);


      }
    });
    return false;
  };
  var GetCloseWoReqNum= function () {

     $.ajax({
       url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetCloseWoReqNum/',
       type:'get',
       dataType: 'json',
       success: function (data) {


           $("#closeWoReqNumRep").html(data.html_closeworeqnumrep_list);


       }
     });
     return false;
   };
   var GetOverdueWoReqNum= function () {

      $.ajax({
        url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetOverdueWoReqNum/',
        type:'get',
        dataType: 'json',
        success: function (data) {


            $("#overdueWoReqNumRep").html(data.html_overdueworeqnumrep_list);


        }
      });
      return false;
    };
   var GetOverdueWoReqNum2= function (loc) {

      $.ajax({
        url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetOverdueWoReqNum2/'+loc,
        type:'get',
        dataType: 'json',
        success: function (data) {


            $("#overdueWoReqNumRep").html(data.html_overdueworeqnumrep_list);

        }
      });
      return false;
    };
    var GetLowItemStock= function () {

       $.ajax({
         url: 'Summery/GetLowItemStock/',
         type:'get',
         dataType: 'json',
         success: function (data) {


             $("#lowItemStock").html(data.html_lowitemstock_list);


         }
       });
       return false;
     };
    var GetRequestedWo= function () {

       $.ajax({
         url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetRequestedWo/',
         type:'get',
         dataType: 'json',
         success: function (data) {


             $("#requestedWo").html(data.html_requestedwo_list);


         }
       });
       return false;
     };
     var GetEmCount= function () {

        $.ajax({
          url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetEmCount/',
          type:'get',
          dataType: 'json',
          success: function (data) {



              $("#EmCount").html(data.html_emwo_list.dt1);


          }
        });
        return false;
      };
     var GetEmCount2= function (loc) {

        $.ajax({
          url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetEmCount2/'+loc,
          type:'get',
          dataType: 'json',
          success: function (data) {



              $("#EmCount").html(data.html_emwo_list.dt1);


          }
        });
        return false;
      };
      var getDueService=function()
      {
        $.ajax({
          url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetdueWoNum/',
          type:'get',
          dataType: 'json',
          success: function (data) {



              $("#dueservice").html(data.html_dueservice_list);

          }
        });
        return false;
      }
      var getDueService2=function()
      {
        $.ajax({
          url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetdueWoNum2/'+loc,
          type:'get',
          dataType: 'json',
          success: function (data) {



              $("#dueservice").html(data.html_dueservice_list);

          }
        });
        return false;
      }
