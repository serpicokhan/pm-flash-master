
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
    // console.log(btn.attr("data-url")+'?q='+$("#id_assetName").val());
    return $.ajax({
      url: btn.attr("data-url")+'?q='+$("#id_makan").val(),
      type: 'get',
      dataType: 'json',
      beforeSend: function (xhr,x) {
        if($("#id_assetName").val()=== null ||$("#id_assetName").val()==='' ){
          toastr.error("مکان را انتخاب نمایید");
          xhr.abort();
          return;
        }

        $("#modal-company").modal("show");

      },
      success: function (data) {
        $("#modal-company .modal-content").html(data.html_ringAmar_form);
        $('#id_assetAmarDate').pDatepicker({
          format: 'YYYY-MM-DD',
          autoClose: true,
          initialValueType: 'gregorian'
        });

      }
    });



};
//$("#modal-company").on("submit", ".js-company-create-form",
var saveForm= function () {
   var form = $(this);
   console.log(form.serialize());

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     errors:function(x,y,z){
       console.log(x);
       console.log(y);
       console.log(z);
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_ringAmar_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_ringAmar_list);
       }
       else {

         $("#company-table tbody").html(data.html_ringAmar_list);
         $("#modal-company .modal-content").html(data.html_ringAmar_form);
       }
     }
   });
   return false;
 };
var applyForm= function () {

   var form = $("#amarform");
   console.log(form.serialize());

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     errors:function(x,y,z){
       console.log(x);
       console.log(y);
       console.log(z);
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_ringAmar_list);
         toastr.success("اطلاعات با موفقت درج شد");
         $("input[type=text][name!=assetAmarDate], textarea").val("");
         $("input[type=number], textarea").val("0");


        // console.log(data.html_ringAmar_list);
       }
       else {
         toastr.error("ورودیهای خود را مجدد چک کنید");

       }
     }
   });
   return false;
 };




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoRingAmarLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initRingAmarFileLoad,initRingAmarAssetLoad,initRingAmarPartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-ringAmar").click(myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-ringAmar", myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-update-form", saveForm);
$("#modal-company").on("click", ".create-next", applyForm);
// Delete book
$("#company-table").on("click", ".js-delete-ringAmar", loadForm);
$("#modal-company").on("submit", ".js-ringAmar-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
