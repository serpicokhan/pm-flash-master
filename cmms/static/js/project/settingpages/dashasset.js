$(function () {

  var loadDashAssetForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-dashAsset").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-dashAsset .modal-content").html(data.html_dashAsset_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveDashAssetForm= function () {


   var form = $(this).parent();
   $.ajax({
     async: true,
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_dashAsset").empty();
         $("#tbody_dashAsset").html(data.html_dashAsset_list);
         $("#modal-dashAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#dashAsset-table tbody").html(data.html_dashAsset_list);
         $("#modal-dashAsset .modal-content").html(data.html_dashAsset_form);
       }
     }
   });
   return false;
 };
 var deleteDashAsset=function(id){
   $.ajax({
     async: true,
     url: '/SettingPage/DashAsset/'+id+'/Delete/',

     type: 'get',
     dataType: 'json',
     success: function (data) {
       console.log(data);
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_dashAsset").empty();
         $("#tbody_dashAsset").html(data.html_dashAsset_list);
         $("#modal-dashAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#dashAsset-table tbody").html(data.html_dashAsset_list);
         $("#modal-dashAsset .modal-content").html(data.html_dashAsset_form);
       }
     }
   });

   return false;
 }
 
  $('#dashAsset-table').on('click','.js-delete-dashAsset', function () {
  const dashassetid=($(this).attr('data-url'));

    swal({
         title: "حذف",
         text: "حذف",
         type: "warning",
         showCancelButton: true,
         confirmButtonColor: "#DD6B55",
         confirmButtonText: "بلی",
         cancelButtonText: "خیر",
         closeOnConfirm: true
     }, function () {
         // cancelform();
         deleteDashAsset(dashassetid);

     });

    // do something…
  });

 // Create book
$(".js-create-dashAsset").click(loadDashAssetForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#dashAsset-table").on("click", ".js-update-dashAsset", loadDashAssetForm);

$("#modal-dashAsset").on("click", ".js-dashAsset-update-form", saveDashAssetForm);
// Delete book
// $("#dashAsset-table").on("click", ".js-delete-dashAsset", loadDashAssetForm);
// $("#modal-dashAsset").on("click", ".js-dashAsset-delete-form", deleteDashAssetForm);

});
