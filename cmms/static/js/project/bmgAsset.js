$(function () {

  var loadBMGAssetForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-bmgAsset").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-bmgAsset .modal-content").html(data.html_bmgAsset_form);
        // $('.selectpicker').selectpicker();
        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.assetCode + "] " + item.assetName,

            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/Asset/GetAssets',
                {
                  data: { 'qry': qry}
                }
              ).done(function (res) {
                // console.log(res);
                callback(res)
              });
            },

          }
        });
        $('.advanced2AutoComplete').on('autocomplete.select', function (evt, item) {
          $("#id_BMGAsset").val(item.id);
          $('#id_BMGAsset').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveBMGAssetForm= function () {

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
         $("#tbody_bmgAsset").empty();
         $("#tbody_bmgAsset").html(data.html_bmgAsset_list);
         $("#modal-bmgAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bmgAsset-table tbody").html(data.html_bmgAsset_list);
         $("#modal-bmgAsset .modal-content").html(data.html_bmgAsset_form);
       }
     }
   });
   return false;
 };
 var deleteBMGAssetForm= function (event) {
   // console.log(event.target.className);
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
          console.log(data);
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_bmgAsset").empty();
          $("#tbody_bmgAsset").html(data.html_bmgAsset_list);
          $('#modal-bmgAsset').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          // $("#task-table tbody").html(data.html_task_list);
          // $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };
 // Create book
$(".js-create-bmgAsset").unbind();
$(".js-create-bmgAsset").click(loadBMGAssetForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#bmgAsset-table").on("click", ".js-update-bmgAsset", loadBMGAssetForm);

$("#modal-bmgAsset").on("submit", ".js-bmgAsset-update-form", loadBMGAssetForm);
// Delete book
$("#bmgAsset-table").on("click", ".js-delete-bmgAsset", loadBMGAssetForm);
$("#modal-bmgAsset").on("submit", ".js-bmgAsset-delete-form", saveBMGAssetForm);
$("#modal-bmgAsset").on("click", ".js-bmgAsset-delete-form", deleteBMGAssetForm);
});
