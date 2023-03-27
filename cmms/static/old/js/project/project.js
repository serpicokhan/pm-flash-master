
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
        // /$("#modal-project").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_project_form);
        $('#id_ProjectStartDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });
        $('#id_ProjectEndDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });
        $('#id_ProjectActualStartDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });
        $('#id_ProjectActualEndDate').pDatepicker({
                        format: 'YYYY-MM-DD',
                        autoClose: true,
                        initialValueType: 'gregorian'
                    });

      }
    });



};
var cancelForm=function(){

  $.ajax({
    url: '/Project/'+$("#lastProjectid").val()+'/Cancel/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_project_list);
        $("tr").on('click',function(){
          getBrief($(this).attr('data-url'));
        });
        // $("#modal-taskGroup").modal("hide");
       // console.log(data.html_taskGroup_list);
      }
      else {

        $("#company-table tbody").html(data.html_project_list);
        $("#modal-company .modal-content").html(data.html_project_form);
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
         $("#tbody_company").html(data.html_project_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_project_list);
       }
       else {

         $("#company-table tbody").html(data.html_project_list);
         $("#modal-company .modal-content").html(data.html_project_form);
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

 var initProjectStockLoad=function(){


   $.ajax({

     url: '/ProjectStock/'+$("#lastProjectid").val()+'/listProjectStock',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_projectStock_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectStock").empty();
         $("#tbody_projectStock").html(data.html_projectStock_list);
         $("#modal-projectStock").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#projectStock-table tbody").html(data.html_projectStock_list);
         $("#modal-projectStock .modal-content").html(data.html_projectStock_form);
       }
     }
   });
return false;
 };
 var initProjectMeterLoad=function(){

   $.ajax({

     url: '/ProjectMeter/'+$("#lastProjectid").val()+'/listProjectMeter',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_projectMeter_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectMeter").empty();
         $("#tbody_projectMeter").html(data.html_projectMeter_list);
         $("#modal-projectMeter").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#projectMeter-table tbody").html(data.html_projectMeter_list);
         $("#modal-projectMeter .modal-content").html(data.html_projectMeter_form);
       }
     }
   });
return false;
 };


 var initProjectScheduledLoad=function(){

   $.ajax({

     url: '/ProjectScheduled/'+$("#lastProjectid").val()+'/listProjectScheduled',



     success: function (data) {

       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_projectEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectScheduled").empty();
         $("#tbody_projectScheduled").html(data.html_projectscheduled_list);

         //console.log(data.html_wo_list);
       }
       else {

         $("#projectScheduled-table tbody").html(data.html_projectScheduled_list);
         //$("#modal-projectEvent .modal-content").html(data.html_projectScheduled_form);
       }
     }
   });
 return false;
 };


 var initProjectWoLoad=function(){

   $.ajax({

     url: '/ProjectWo/'+$("#lastProjectid").val()+'/listProjectWo',



     success: function (data) {

       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_projectEvent_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectWo").empty();
         $("#tbody_projectWo").html(data.html_projectWo_list);

         //console.log(data.html_wo_list);
       }
       else {

         $("#projectWo-table tbody").html(data.html_projectWo_list);
         //$("#modal-projectEvent .modal-content").html(data.html_projectWo_form);
       }
     }
   });
 return false;
 };



 var initProjectUserLoad=function(){

   $.ajax({

     url: '/ProjectUser/'+$("#lastProjectid").val()+'/listProjectUser',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectUser").empty();
         $("#tbody_projectUser").html(data.html_projectUser_list);
         $("#modal-projectUser").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#projectUser-table tbody").html(data.html_projectUser_list);
         $("#modal-projectUser .modal-content").html(data.html_projectUser_form);
       }
     }
   });
 return false;
 };


 var initProjectFileLoad=function(){

   $.ajax({

     url: '/ProjectFile/'+$("#lastProjectid").val()+'/listProjectFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_projectFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_projectFile").empty();
         $("#tbody_projectFile").html(data.html_projectFile_list);
         $("#modal-projectFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#projectFile-table tbody").html(data.html_projectFile_list);
         $("#modal-projectFile .modal-content").html(data.html_projectFile_form);
       }
     }
   });
 return false;
 };


  var initProjectPartLoad=function(){

    $.ajax({

      url: '/ProjectPart/'+$("#lastProjectid").val()+'/listProjectPart',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_projectPart_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_projectPart").empty();
          $("#tbody_projectPart").html(data.html_projectPart_list);
          $("#modal-projectPart").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#projectPart-table tbody").html(data.html_projectPart_list);
          $("#modal-projectPart .modal-content").html(data.html_projectPart_form);
        }
      }
    });
  return false;
  };

  var initProjectAssetLoad=function(){

    $.ajax({

      url: '/ProjectAsset/'+$("#lastProjectid").val()+'/listProjectAsset',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_projectProject_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_projectAsset").empty();
          $("#tbody_projectAsset").html(data.html_projectAsset_list);
          $("#modal-projectAsset").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#projectAsset-table tbody").html(data.html_projectAsset_list);
          $("#modal-projectAsset .modal-content").html(data.html_projectAsset_form);
        }
      }
    });
  return false;
  };


    var initProjectPurchaseLoad=function(){

      $.ajax({

        url: '/ProjectPurchase/'+$("#lastProjectid").val()+'/listProjectPurchase',



        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_projectPurchase_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_projectPurchase").empty();
            $("#tbody_projectPurchase").html(data.html_projectPurchase_list);
            $("#modal-projectPurchase").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#projectPurchase-table tbody").html(data.html_projectPurchase_list);
            $("#modal-projectPurchase .modal-content").html(data.html_projectPurchase_form);
          }
        }
      });
    return false;
    };

    var initProjectLocationLoad=function(){

      $.ajax({

        url: '/ProjectLocation/'+$("#lastProjectid").val()+'/listProjectLocation ',

        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_projectLocation_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_projectLocation").empty();
            $("#tbody_projectLocation").html(data.html_projectLocation_list);
            $("#modal-projectLocation").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            $("#projectLocation-table tbody").html(data.html_projectLocation_list);
            $("#modal-projectLocation.modal-content").html(data.html_projectLocation_form);
          }
        }
      });
    return false;
    };



 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoProjectLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initProjectScheduledLoad,initProjectWoLoad,initProjectUserLoad,initProjectFileLoad);
   //loadForm(btn);

   //initLoad();
 }
 var searchProject=function(searchStr){
   searchStr=searchStr.replace(' ','_')
   if(searchStr.length==0)
      searchStr='empty_';
      $.ajax({

        url: '/Project/'+searchStr+'/Search/ ',

        success: function (data) {
            //alert($("#lastWorkOrderid").val());
          if (data.form_is_valid) {


            //alert(data.html_projectLocation_list);  // <-- This is just a placeholder for now for testing
            $("#tbody_company").empty();
            $("#tbody_company").html(data.html_projectLocation_list);
            $("tr").on('click',function(){
              getBrief($(this).attr('data-url'));
            });
            // getBrief($(this).attr('data-url'));
            // $("#modal-projectLocation").modal("hide");
            //console.log(data.html_wo_list);
          }
          else {

            // $("#tbody_company").html(data.html_projectLocation_list);
            // $("#modal-projectLocation.modal-content").html(data.html_projectLocation_form);
          }
        }
      });
    return false;

 }
 $("#searchProject").on('input',function(){
   searchProject($("#searchProject").val());
 });
var getBrief= function(id)
{
  console.log($(this).find("td:eq(1)").text());
  $("#projectName").html($(this).find("td:eq(1)").text());
  $.ajax({

    url: '/Project/'+id+'/brief/ ',

    success: function (data) {
        //alert($("#lastWorkOrderid").val());
      if (data.form_is_valid) {


        //alert(data.html_projectLocation_list);  // <-- This is just a placeholder for now for testing
        // $("#tbody_company").empty();
        $("#projectWO").html(data.projectWoCount);
        $("#projectSWO").html(data.projectSWoCount);
        $("#projectHour").html(data.projectHour);
        $("#projectCompletion").html(data.projectWoCountoverall+'%');
        $("#projectCompletionOnTime").html(data.projectWoCountontime+'%');
        $("#projectCost").html(data.totalCost+' ریال');
        // $("#modal-projectLocation").modal("hide");
        //console.log(data.html_wo_list);
      }
      else {

        // $("#tbody_company").html(data.html_projectLocation_list);
        // $("#modal-projectLocation.modal-content").html(data.html_projectLocation_form);
      }
    }
  });
return false;

}
$("tr").on('click',function(){
  getBrief($(this).attr('data-url'));
});


$(".js-create-project").click(myWoLoader);
$("#modal-company").on("submit", ".js-project-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-project", myWoLoader);
$("#modal-company").on("submit", ".js-project-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-project", loadForm);
$("#modal-company").on("submit", ".js-project-delete-form", saveForm);
$('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
