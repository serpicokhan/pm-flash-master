$(function () {

  var loadBMGTemplateForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-bmgTemplate").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-bmgTemplate .modal-content").html(data.html_bmgTemplate_form);
        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          formatResult: function (item) {
            return {
              value: item.id,
              text:  item.assetMeterTemplateDesc ,

            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/AssetMeterTemplate/GetAssetMeterTemplates',
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
          $("#id_BMGTemplate").val(item.id);
          $('#id_BMGTemplate').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveBMGTemplateForm= function () {

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
         $("#tbody_bmgTemplate").empty();
         $("#tbody_bmgTemplate").html(data.html_bmgTemplate_list);
         $("#modal-bmgTemplate").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#bmgTemplate-table tbody").html(data.html_bmgTemplate_list);
         $("#modal-bmgTemplate .modal-content").html(data.html_bmgTemplate_form);
       }
     }
   });
   return false;
 };
 var deleteBMGTemplateForm= function (event) {
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
          $("#tbody_bmgTemplate").empty();
          $("#tbody_bmgTemplate").html(data.html_bmgTemplate_list);
          $('#modal-bmgTemplate').modal('hide');

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
$(".js-create-bmgTemplate").unbind();
$(".js-create-bmgTemplate").click(loadBMGTemplateForm);
//$d("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#bmgTemplate-table").on("click", ".js-update-bmgTemplate", loadBMGTemplateForm);

$("#modal-bmgTemplate").on("submit", ".js-bmgTemplate-update-form", loadBMGTemplateForm);
// Delete book
$("#bmgTemplate-table").on("click", ".js-delete-bmgTemplate", loadBMGTemplateForm);
$("#modal-bmgTemplate").on("submit", ".js-bmgTemplate-delete-form", saveBMGTemplateForm);
$("#modal-bmgTemplate").on("click", ".js-bmgTemplate-delete-form", deleteBMGTemplateForm);
});
