
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
        // alert(btn.attr("data-url"));
        //alert("321321");
        // /$("#modal-miniWorkorder").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        console.log(data);
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_miniWorkorder_form);
          $('.selectpicker').selectpicker();
          $('.basicAutoComplete').autoComplete();

      },
      error:function(x,y,z){
        console.log(x,y,z);
      }

    });



};
  var loadForm2 =function (btn1) {
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
        // /$("#modal-miniWorkorder").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_miniWorkorder_form);
          $('.selectpicker').selectpicker();

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
         $("#tbody_company").html(data.html_miniWorkorder_list);
         $("#modal-company").modal("hide");
          toastr.success("عملیات با موفقیت انجام شد");
        // console.log(data.html_miniWorkorder_list);
       }
       else {

         $("#company-table tbody").html(data.html_miniWorkorder_list);
         $("#modal-company .modal-content").html(data.html_miniWorkorder_form);
         toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");

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



   //$.when(loadForm(btn)).done(initLoad,initWoMiniWorkorderLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initMiniWorkorderFileLoad,initMiniWorkorderAssetLoad,initMiniWorkorderPartLoad );
   loadForm(btn);

   //initLoad();
 }
 var myWoLoader2= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoMiniWorkorderLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initMiniWorkorderFileLoad,initMiniWorkorderAssetLoad,initMiniWorkorderPartLoad );
   loadForm(btn);

   //initLoad();
 }




$(".js-create-miniWorkorder").click(myWoLoader);
$("#modal-company").on("submit", ".js-miniWorkorder-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-miniWorkorder", myWoLoader);
$("#company-table").on("click", "tr", myWoLoader);
$("#modal-company").on("submit", ".js-miniWorkorder-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-miniWorkorder", loadForm);
$("#modal-company").on("submit", ".js-miniWorkorder-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
