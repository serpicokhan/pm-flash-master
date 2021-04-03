var GetWoPartNum= function () {

   $.ajax({
     url: 'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoPartNum/',
     type:'get',
     dataType: 'json',
     success: function (data) {

         // alert(ompany created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_company").empty();
         // console.log(data);
         $("#monthlyWoPartNumRep").html(data.html_monthlywopartnumrep_list);
         //$("#modal-company").modal("hide");
         //console.log(data.html_order_list);


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

         // alert(ompany created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_company").empty();
         // console.log(data);
         $("#stopNumRep").html(data.html_stopnumrep_list);
         //$("#modal-company").modal("hide");
         //console.log(data.html_order_list);


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

          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          //$("#tbody_company").empty();
          // console.log("'Summery/'+$("#dashboardt1").val()+'/'+$("#dashboardt2").val()+'/GetWoReqNum/'");
          // console.log(data.html_monthlyworeqnumrep_list);
          // console.log("tamam");
          $("#monthlyWoReqNumRep").html(data.html_monthlyworeqnumrep_list);
          //$("#modal-company").modal("hide");
          //console.log(data.html_order_list);


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

      //alert("Company created!");  // <-- This is just a placeholder for now for testing
      //$("#tbody_company").empty();
      $("#monthlyMTTR").html(data.html_monthlymttrrep_list);
      //$("#modal-company").modal("hide");
      //console.log(data.html_order_list);


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

         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_company").empty();
         $("#monthlyMisc").html(data.html_monthlymiscrep_list);
         //$("#modal-company").modal("hide");
         //console.log(data.html_order_list);


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
       // console.log("darkhast bala");
       // console.log(data);
       // console.log("tamam");

         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_company").empty();
         $("#HighPriorityWO").html(data.html_highprioritywo_list);
         //$("#modal-company").modal("hide");
         //console.log(data.html_order_list);


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

          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          //$("#tbody_company").empty();
          $("#openWoReqNumRep").html(data.html_openworeqnumrep_list);
          //$("#modal-company").modal("hide");
          //console.log(data.html_order_list);
        //console.log(data);

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

           //alert("Company created!");  // <-- This is just a placeholder for now for testing
           //$("#tbody_company").empty();
           $("#closeWoReqNumRep").html(data.html_closeworeqnumrep_list);
           //$("#modal-company").modal("hide");
           //console.log(data.html_order_list);
         //console.log(data);

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

            //alert("Company created!");  // <-- This is just a placeholder for now for testing
            //$("#tbody_company").empty();
            $("#overdueWoReqNumRep").html(data.html_overdueworeqnumrep_list);
            //$("#modal-company").modal("hide");
            //console.log(data.html_order_list);
          //console.log(data);

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

             //alert("Company created!");  // <-- This is just a placeholder for now for testing
             //$("#tbody_company").empty();
             $("#lowItemStock").html(data.html_lowitemstock_list);
             //$("#modal-company").modal("hide");
             //console.log(data.html_order_list);
           //console.log(data);

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

             //alert("Company created!");  // <-- This is just a placeholder for now for testing
             //$("#tbody_company").empty();
             $("#requestedWo").html(data.html_requestedwo_list);
             //$("#modal-company").modal("hide");
             //console.log(data.html_order_list);
           //console.log(data);

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
            console.log(data);

              //alert("Company created!");  // <-- This is just a placeholder for now for testing
              //$("#tbody_company").empty();
              $("#EmCount").html(data.html_emwo_list.dt1);
              //$("#modal-company").modal("hide");
              //console.log(data.html_order_list);
            //console.log(data);

          }
        });
        return false;
      };
