$(function () {

  var loadAssetExceptionForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetException").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-assetException .modal-content").html(data.html_assetException_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetExceptionForm= function () {


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
         $("#tbody_assetException").empty();
         $("#tbody_assetException").html(data.html_assetException_list);
         $("#modal-assetException").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetException-table tbody").html(data.html_assetException_list);
         $("#modal-assetException .modal-content").html(data.html_assetException_form);
       }
     }
   });
   return false;
 };
 var deleteAssetExceptionForm= function (event) {

    var form = $(this);
    if(event.target.className=="btn btn-danger")
    {
    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_assetException").empty();
          $("#tbody_assetException").html(data.html_assetException_list);
          $("#modal-assetException").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetException-table tbody").html(data.html_assetException_list);
          $("#modal-assetException .modal-content").html(data.html_assetException_form);
        }
      }
    });
  }
    return false;
  };
  var deleteAssetException=function(id){
    $.ajax({
      async: true,
      url: '/SettingPage/AssetException/'+id+'/Delete/',

      type: 'get',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_assetException").empty();
          $("#tbody_assetException").html(data.html_assetException_list);
          $("#modal-assetException").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {


        }
      }
    });

    return false;
  }
  $('#assetException-table').on('click','.js-delete-assetException', function () {
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
         deleteAssetException(dashassetid);

     });

    // do something…
  });

 // Create book
$(".js-create-assetException").click(loadAssetExceptionForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetException-table").on("click", ".js-update-assetException", loadAssetExceptionForm);

$("#modal-assetException").on("click", ".js-assetException-update-form", saveAssetExceptionForm);
// Delete book
// $("#assetException-table").on("click", ".js-delete-assetException", loadAssetExceptionForm);
// $("#modal-assetException").on("click", ".js-assetException-delete-form", deleteAssetExceptionForm);

});
