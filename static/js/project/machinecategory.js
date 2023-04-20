
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
        // /$("#modal-machineCategory").modal("hide");
        $("#modal-machineCategory").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-machineCategory .modal-content").html(data.html_machineCategory_form);

      }
    });



};
//$("#modal-machineCategory").on("submit", ".js-company-create-form",
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
         $("#tbody_mcategory").empty();
         $("#tbody_mcategory").html(data.html_machineCategory_list);
         $("#modal-machineCategory").modal("hide");
        // console.log(data.html_machineCategory_list);
       }
       else {

         $("#company-table tbody").html(data.html_machineCategory_list);
         $("#modal-machineCategory .modal-content").html(data.html_machineCategory_form);
       }
     }
   });
   return false;
 };
/*
 $('#modal-machineCategory').on('hidden.bs.modal', function () {
   alert("321321");
   console.log($("#lastWorkOrderid").val());
   $.ajax({
     url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/deleteChildren',



     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         //$("#tbody_mcategory").empty();
         //$("#tbody_mcategory").html(data.html_wo_list);
         //$("#modal-machineCategory").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#company-table tbody").html(data.html_wo_list);
         $("#modal-machineCategory .modal-content").html(data.html_form);
       }
     }
   });


  // do something…
});
*/
 //alert("321312");
 // Create book




 var myWoLoader= function(){
   btn=$(this);
   //alert("dsds");



   //$.when(loadForm(btn)).done(initLoad,initWoAssetCategoryLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initAssetCategoryFileLoad,initAssetCategoryAssetLoad,initAssetCategoryPartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-machineCategory").click(myWoLoader);
$("#modal-machineCategory").on("submit", ".js-machineCategory-create-form", saveForm);

// Update book
$("#machineCategory-table").on("click", ".js-update-machineCategory", myWoLoader);
$("#modal-machineCategory").on("submit", ".js-machineCategory-update-form", saveForm);
// Delete book
$("#machineCategory-table").on("click", ".js-delete-machineCategory", loadForm);
$("#modal-machineCategory").on("submit", ".js-machineCategory-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
