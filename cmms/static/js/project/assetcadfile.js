
$(function () {

  var search=function(qstr){
    window.location=`/AssetCadFile/Search?qstr=${qstr}`;
  }
  $('.btn-search').click(function(){
    console.log("work!");
    if($("#assetSearch").val()!=='')
      search($("#assetSearch").val());
    else {
      window.location=`/AssetCadFile/`;
    }
  });
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

        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_assetCadFile_form);
        $(".selectpicker").selectpicker();

      }
    });



};
//$("#modal-company").on("submit", ".js-company-create-form",
var saveForm= function (e) {
  var form2 = $(this);

  var form = new FormData(document.getElementById("assetusercadformid"));

   $.ajax({
     url: form2.attr("action"),
     data: form,
     type: form2.attr("method"),
     dataType: 'json',
     cache:false,
     contentType: false,
     processData: false,
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_assetCadFile_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_assetCadFile_list);
       }
       else {

         toastr.error(data.error);
       }
     }
   });
   return false;
 };
var saveForm2= function (e) {
  var form = $(this);

  // var form = new FormData(document.getElementById("assetusercadformid"));
  // e.preventDefault();

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',

     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_assetCadFile_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_assetCadFile_list);
       }
       else {

         $("#company-table tbody").html(data.html_assetCadFile_list);
         $("#modal-company .modal-content").html(data.html_assetCadFile_form);
       }
     }
   });
   return false;
 };




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoAssetCadFileLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initAssetCadFileFileLoad,initAssetCadFileAssetLoad,initAssetCadFilePartLoad );
   loadForm(btn);

   //initLoad();
 }



$(".js-create-assetCadFile").click(myWoLoader);
$("#modal-company").on("submit", ".js-AssetCadFile-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-assetCadFile", myWoLoader);
$("#modal-company").on("submit", ".js-assetCadFile-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-assetCadFile", loadForm);
$("#modal-company").on("submit", ".js-assetCadFile-delete-form", saveForm2);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
