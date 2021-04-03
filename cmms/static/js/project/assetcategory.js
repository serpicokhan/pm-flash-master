
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
        // /$("#modal-assetCategory").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_assetCategory_form);

      }
    });



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
         $("#tbody_company").html(data.html_assetCategory_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_assetCategory_list);
       }
       else {

         $("#company-table tbody").html(data.html_assetCategory_list);
         $("#modal-company .modal-content").html(data.html_assetCategory_form);
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




 var myWoLoader= function(){
   btn=$(this);
   //alert("dsds");



   //$.when(loadForm(btn)).done(initLoad,initWoAssetCategoryLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initAssetCategoryFileLoad,initAssetCategoryAssetLoad,initAssetCategoryPartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-assetCategory").click(myWoLoader);
$("#modal-company").on("submit", ".js-assetCategory-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-assetCategory", myWoLoader);
$("#modal-company").on("submit", ".js-assetCategory-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-assetCategory", loadForm);
$("#modal-company").on("submit", ".js-assetCategory-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
