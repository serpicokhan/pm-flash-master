$(function () {

  var loadBOMGroupAssetForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-bomGroupAsset").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-bomGroupAsset .modal-content").html(data.html_bomGroupAsset_form);
        $('.selectpicker').selectpicker();
        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.id + "] " + item.partName,

            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/WoPart/GetParts',
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
          $("#id_bomGroupAssetPid").val(item.id);
          $('#id_bomGroupAssetPid').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveBOMGroupAssetForm= function () {

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
 var deleteBOMGroupAssetForm= function (event) {
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
          $("#tbody_bomGroupAsset").empty();
          $("#tbody_bomGroupAsset").html(data.html_bomGroupAsset_list);
          $('#modal-bomGroupAsset').modal('hide');

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
$(".js-create-bomGroupAsset").unbind();
$(".js-create-bomGroupAsset").click(loadBOMGroupAssetForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#bomGroupAsset-table").on("click", ".js-update-bomGroupAsset", loadBOMGroupAssetForm);

$("#modal-bomGroupAsset").on("submit", ".js-bomGroupAsset-update-form", loadBOMGroupAssetForm);
// Delete book
$("#bomGroupAsset-table").on("click", ".js-delete-bomGroupAsset", loadBOMGroupAssetForm);
$("#modal-bomGroupAsset").on("submit", ".js-bomGroupAsset-delete-form", saveBOMGroupAssetForm);
$("#modal-bomGroupAsset").on("click", ".js-bomGroupAsset-delete-form", deleteBOMGroupAssetForm);
});
