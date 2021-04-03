$(function () {

  var loadtaskGroupAssetCategoryForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-taskGroupAssetCategory").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-taskGroupAssetCategory .modal-content").html(data.html_taskGroupAssetCategory_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var savetaskGroupAssetCategoryForm= function () {

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
         $("#tbody_taskGroupAssetCategory").empty();
         $("#tbody_taskGroupAssetCategory").html(data.html_taskGroupAssetCategory_list);
         $("#modal-taskGroupAssetCategory").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#taskGroupAssetCategory-table tbody").html(data.html_taskGroupAssetCategory_list);
         $("#modal-taskGroupAssetCategory .modal-content").html(data.html_taskGroupAssetCategory_form);
       }
     }
   });
   return false;
 };
 var deleteTaskGroupAssetCategoryForm= function (event) {

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
          $("#tbody_taskGroupAssetCategory").empty();
          $("#tbody_taskGroupAssetCategory").html(data.html_taskGroupAssetCategory_list);
          $('#modal-taskGroupAssetCategory').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          $("#taskGroupAssetCategory-table tbody").html(data.html_taskGroupAssetCategory_list);
          $("#modal-taskGroupAssetCategory .modal-content").html(data.html_taskGroupAssetCategory_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-taskGroupAssetCategory").click(loadtaskGroupAssetCategoryForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#taskGroupAssetCategory-table").on("click", ".js-update-taskGroupAssetCategory", loadtaskGroupAssetCategoryForm);

$("#modal-taskGroupAssetCategory").on("submit", ".js-taskGroupAssetCategory-update-form", loadtaskGroupAssetCategoryForm);
// Delete book
$("#taskGroupAssetCategory-table").on("click", ".js-delete-taskGroupAssetCategory", loadtaskGroupAssetCategoryForm);
$("#modal-taskGroupAssetCategory").on("click", ".js-taskGroupAssetCategory-delete-form", deleteTaskGroupAssetCategoryForm);

});
