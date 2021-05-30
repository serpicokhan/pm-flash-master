
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
        // /$("#modal-bomgroup").modal("hide");
        $("#modal-company").modal("show");
      },
      success: function (data) {
        //alert("3123@!");
        $("#modal-company .modal-content").html(data.html_bomgroup_form);

      }
    });



};
var cancelForm=function(){
// alert("!23");
  $.ajax({
    url: '/BOMGroup/'+$("#lastBOMGroupid").val()+'/Cancel/',

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_bomgroup_list);


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

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_bomgroup_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_bomgroup_list);
       }
       else {

         $("#company-table tbody").html(data.html_bomgroup_list);
         $("#modal-company .modal-content").html(data.html_bomgroup_form);
       }
     }
   });
   return false;
 };
 var initBOMGroupPart=function(){


   $.ajax({

     url: '/BOMGroupPart/'+$("#lastBOMGroupid").val()+'/listBOMGroupPart',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_bomGroupPart_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_bomGroupPart").empty();
         $("#tbody_bomGroupPart").html(data.html_bomGroupPart_list);
         $("#modal-bomGroupPart").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bomGroupPart-table tbody").html(data.html_bomGroupPart_list);
         $("#modal-bomGroupPart .modal-content").html(data.html_bomGroupPart_form);
       }
     }
   });
return false;
 };

 var initBOMGroupAsset=function(){


   $.ajax({

     url: '/BOMGroupAsset/'+$("#lastBOMGroupid").val()+'/listBOMGroupAsset',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {
         //alert("response");
         //alert(data.html_bomGroupAsset_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_bomGroupAsset").empty();
         $("#tbody_bomGroupAsset").html(data.html_bomGroupAsset_list);
         $("#modal-bomGroupAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bomGroupAsset-table tbody").html(data.html_bomGroupAsset_list);
         $("#modal-bomGroupAsset .modal-content").html(data.html_bomGroupAsset_form);
       }
     }
   });
return false;
 };




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoBOMGroupLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   $.when(loadForm(btn)).done(initBOMGroupPart,initBOMGroupAsset );
   // loadForm(btn);

   //initLoad();
 }


$(".js-create-bomgroup").unbind();
$(".js-create-bomgroup").click(myWoLoader);
$("#modal-company").on("submit", ".js-bomgroup-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-bomgroup", myWoLoader);
$("#modal-company").on("submit", ".js-bomgroup-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-bomgroup", loadForm);
$("#modal-company").on("submit", ".js-bomgroup-delete-form", saveForm);
// $('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
