
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
        // /$("#modal-batchMeterGroup").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_batchMeterGroup_form);

      }
    });



};
var cancelForm=function(){
// alert("!23");
  $.ajax({
    url: '/BatchMeterGroup/'+$("#lastBatchMeterGroupid").val()+'/Cancel/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_batchMeterGroup_list);


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
   var xxx=form.serialize();

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(){
       console.log(xxx);
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_batchMeterGroup_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_batchMeterGroup_list);
       }
       else {

        if(data.bom_error){
          toastr.error(data.bom_error);
        }
       }
     }
   });
   return false;
 };
 var initBatchMeterGroupAsset=function(){


   $.ajax({

     url: '/BMGAsset/'+$("#lastBatchMeterGroupid").val()+'/listBMGAsset',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_bomGroupPart_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_bmgAsset").empty();
         $("#tbody_bmgAsset").html(data.html_bmgAsset_list);
         $("#modal-bmgAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bmgAsset-table tbody").html(data.html_bmgAsset_list);
         $("#modal-bmgAsset .modal-content").html(data.html_bmgAsset_form);
       }
     }
   });
return false;
 };

 var initBatchMeterGroupTemplate=function(){


   $.ajax({

     url: '/BMGTemplate/'+$("#lastBatchMeterGroupid").val()+'/listBMGTemplate',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_bmgTemplate_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_bmgTemplate").empty();
         $("#tbody_bmgTemplate").html(data.html_bmgTemplate_list);
         $("#modal-bmgTemplate").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bmgTemplate-table tbody").html(data.html_bmgTemplate_list);
         $("#modal-bmgTemplate .modal-content").html(data.html_bmgTemplate_form);
       }
     }
   });
return false;
 };




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoBatchMeterGroupLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initBatchMeterGroupTemplate,initBatchMeterGroupAsset );
   // loadForm(btn);

   //initLoad();
 }
 ////////////////Search buttom click#############################
 var searchBOM= function (searchStr) {


    $.ajax({
      url: '/BatchMeterGroup/'+searchStr+'/Search/',

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {


          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_bom_search_tag_list);
          $(".woPaging").html(data.html_bom_paginator);

          $("#modal-company").modal("hide");

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

  $('#bomSearch').keyup(function(){

   searchStr=$("#bomSearch").val();

   searchStr=searchStr.replace(' ','_');

   if(searchStr.trim().length>0){
   searchBOM(searchStr);
 }
 else {
   searchBOM('empty');


 }
    // alert("salam");

 });
 ////////////////////////////////////////////////////////////////


$(".js-create-batchMeterGroup").unbind();
$(".js-create-batchMeterGroup").click(myWoLoader);
$("#modal-company").on("submit", ".js-batchMeterGroup-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-batchMeterGroup", myWoLoader);
$("#modal-company").on("submit", ".js-batchMeterGroup-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-batchMeterGroup", loadForm);
$("#modal-company").on("submit", ".js-batchMeterGroup-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
