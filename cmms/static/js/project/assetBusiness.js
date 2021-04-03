$(function () {

  var loadAssetBusinessForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetBusiness").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetBusinessForm= function () {

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
         $("#tbody_assetBusiness").empty();
         $("#tbody_assetBusiness").html(data.html_assetBusiness_list);
         $("#modal-assetBusiness").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetBusiness-table tbody").html(data.html_assetBusiness_list);
         $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
       }
     }
   });
   return false;
 };
 var deleteAssetBusinessForm= function (event) {
   console.log(event.target.className);
   if(event.target.className=="btn btn-danger")
   {

    var form = $(this);


    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_assetBusiness").empty();
          $("#tbody_assetBusiness").html(data.html_assetBusiness_list);
          $("#modal-assetBusiness").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetBusiness-table tbody").html(data.html_assetBusiness_list);
          $("#modal-assetBusiness .modal-content").html(data.html_assetBusiness_form);
        }
       }
    });
  }
    return false;
  };

 // Create book
$(".js-create-assetBusiness").click(loadAssetBusinessForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetBusiness-table").on("click", ".js-update-assetBusiness", loadAssetBusinessForm);

$("#modal-assetBusiness").on("submit", ".js-assetBusiness-update-form", loadAssetBusinessForm);
// Delete book
$("#assetBusiness-table").on("click", ".js-delete-assetBusiness", loadAssetBusinessForm);
$("#modal-assetBusiness").on("click", ".js-assetBusiness-delete-form", deleteAssetBusinessForm);

});
