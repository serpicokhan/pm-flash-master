
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
        // /$("#modal-taskGroup").modal("hide");
          $("#modal-taskGroup").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-taskGroup .modal-content").html(data.html_taskGroup_form);

      }
    });



};
var searchPart= function (searchStr) {


   $.ajax({
     url: '/TaskGroup/'+searchStr+'/Search/',

     type: 'GET',
     dataType: 'json',
     success: function (data) {

       if (data.form_is_valid) {


         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();

         $("#tbody_company").html(data.html_taskGroup_list);
         $(".woPaging").html("");

         // $("#modal-company").modal("hide");
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

 $('#txttaskgroupsearch').keyup(function(){

  searchStr=$("#txttaskgroupsearch").val();

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

var cancelForm=function(){

  $.ajax({
    url: '/TaskGroup/'+$("#lastTaskGroupid").val()+'/Cancel/',

    type: 'post',
    dataType: 'json',
    success: function (data) {

      console.log(data.form_is_valid);
      if(data.form_is_valid)
      {
        swal("?????? ????!", $("#id_taskGroupName").val(), "success");




      }
      else {

      }

    }

  });




};
var check_task_num=function(id){
  var result=0;
  $.ajax({
    url: '/TaskGroup/'+$("#lastTaskGroupid").val()+'/check_task_num/',

    type: 'post',
    dataType: 'json',
    success: function (data) {
      // console.log(data);
      if(data.form_is_valid)
      {
        result=data.result



      }
      else {
        result=0;
      }

    }

  });
return result;


}
$('#modal-taskGroup').on('click','.tclose', function () {
  if(check_task_num($("#lastTaskGroupid").val())==0 && $("#id_taskGroupName").val()=="" ){
  swal({
       title: "?????? ???????????? ???????? ???? ?????????? ????????????",
       text: $("#id_taskGroupName").val(),
       type: "warning",
       showCancelButton: true,
       confirmButtonColor: "#DD6B55",
       confirmButtonText: "??????",
       cancelButtonText: "??????",
       closeOnConfirm: true
   }, function () {

       cancelForm();

   });
 }
  // do something???
});
//$("#modal-taskGroup").on("submit", ".js-taskGroup-create-form",
var saveForm= function () {
   var form = $(this);

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_taskGroup_list);
         $("#modal-taskGroup").modal("hide");
         $("#issavechanged").val("1");
        // console.log(data.html_taskGroup_list);
       }
       else {

         $("#company-table tbody").html(data.html_taskGroup_list);
         $("#modal-taskGroup .modal-content").html(data.html_taskGroup_form);
       }
     }
   });
   return false;
 };




 var initTaskGroupFileLoad=function(){

   $.ajax({

     url: '/TaskGroupFile/'+$("#lastTaskGroupid").val()+'/listTaskGroupFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_taskGroupFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_taskGroupFile").empty();
         $("#tbody_taskGroupFile").html(data.html_taskGroupFile_list);
         $("#modal-taskGroupFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#taskGroupFile-table tbody").html(data.html_taskGroupFile_list);
         $("#modal-taskGroupFile .modal-content").html(data.html_taskGroupFile_form);
       }
     }
   });
 return false;
 };


  var initTaskGroupTemplateLoad=function(){

    $.ajax({

      url: '/TaskTemplate/'+$("#lastTaskGroupid").val()+'/listTaskTemplate',



      success: function (data) {
        console.log(data);
          //alert($("#lastWorkOrderid").val());




          //alert(data.html_taskGroupPart_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_taskTemplate").empty();
          $("#tbody_taskTemplate").html(data.html_taskTemplate_list);
          $("#modal-taskTemplate").modal("hide");
          //console.log(data.html_wo_list);

      }
    });
  return false;
  };
  var initTaskGroupAssetCategoryLoad=function(){

    $.ajax({

      url: '/TaskGroupAssetCategory/'+$("#lastTaskGroupid").val()+'/listTaskGroupAssetCategory',



      success: function (data) {
        console.log(data);
          //alert($("#lastWorkOrderid").val());




          //alert(data.html_taskGroupPart_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_taskGroupAssetCategory").empty();
          $("#tbody_taskGroupAssetCategory").html(data.html_taskGroupAssetCategory_list);
          $("#modal-taskGroupAssetCategory").modal("hide");
          //console.log(data.html_wo_list);

      }
    });
  return false;
  };

  var initTaskGroupAssetLoad=function(){

    $.ajax({

      url: '/TaskGroupAsset/'+$("#lastTaskGroupid").val()+'/listTaskGroupAsset',



      success: function (data) {
          //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_taskGroupTaskGroup_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_taskGroupAsset").empty();
          $("#tbody_taskGroupAsset").html(data.html_taskGroupAsset_list);
          $("#modal-taskGroupAsset").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#taskGroupAsset-table tbody").html(data.html_taskGroupAsset_list);
          $("#modal-taskGroupAsset .modal-content").html(data.html_taskGroupAsset_form);
        }
      }
    });
  return false;
  };






 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoTaskGroupLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initTaskGroupTemplateLoad );
   //loadForm(btn);

   //initLoad();
 }



$(".js-create-taskGroup").click(myWoLoader);
// $(".cancel").on('click',cancelForm);
// $('#modal-taskGroup').on('hidden.bs.modal',cancelForm);
$("#modal-taskGroup").on("submit", ".js-taskGroup-create-form", saveForm);


// Update book
$("#company-table").on("click", ".js-update-taskGroup", myWoLoader);
$("#modal-taskGroup").on("submit", ".js-taskGroup-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-taskGroup", loadForm);
$("#modal-taskGroup").on("submit", ".js-taskGroup-delete-form", saveForm);
//$("#taskGroup-table").on("click", ".js-update-wo", initxLoad);
});
