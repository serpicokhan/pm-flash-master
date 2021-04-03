$(function () {

  var loadAssetPartForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetPart").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetPart .modal-content").html(data.html_assetPart_form);
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
                console.log(res);
                callback(res)
              });
            },

          }
        });
        $('.advanced2AutoComplete').on('autocomplete.select', function (evt, item) {
          $("#id_assetPartPid").val(item.id);
          $('#id_assetPartPid').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetPartForm= function () {

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
         $("#tbody_assetPart").empty();
         $("#tbody_assetPart").html(data.html_assetPart_list);
         $("#modal-assetPart").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetPart-table tbody").html(data.html_assetPart_list);
         $("#modal-assetPart .modal-content").html(data.html_assetPart_form);
       }
     }
   });
   return false;
 };
 var deleteAssetPartForm= function (event) {
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
          $("#tbody_assetPart").empty();
          $("#tbody_assetPart").html(data.html_assetPart_list);
          $('#modal-assetPart').modal('hide');

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
$(".js-create-assetPart").unbind();
$(".js-create-assetPart").click(loadAssetPartForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#assetPart-table").on("click", ".js-update-assetPart", loadAssetPartForm);

$("#modal-assetPart").on("submit", ".js-assetPart-update-form", loadAssetPartForm);
// Delete book
$("#assetPart-table").on("click", ".js-delete-assetPart", loadAssetPartForm);
$("#modal-assetPart").on("submit", ".js-assetPart-delete-form", saveAssetPartForm);
$("#modal-assetPart").on("click", ".js-assetPart-delete-form", deleteAssetPartForm);
});
