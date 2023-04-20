$(function () {

  var loadBusinessPartForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-businessPart").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-businessPart .modal-content").html(data.html_businessPart_form);
        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          minChars:1,
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
          $("#id_BusinessPartPart").val(item.id);
          $('#id_BusinessPartPart').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveBusinessPartForm= function () {

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
         $("#tbody_businessPart").empty();
         $("#tbody_businessPart").html(data.html_businessPart_list);
         $("#modal-businessPart").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#businessPart-table tbody").html(data.html_businessPart_list);
         $("#modal-businessPart .modal-content").html(data.html_businessPart_form);
       }
     }
   });
   return false;
 };

 // Create book
$(".js-create-businessPart").unbind();
$(".js-create-businessPart").click(loadBusinessPartForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#businessPart-table").on("click", ".js-update-businessPart", loadBusinessPartForm);

$("#modal-businessPart").on("submit", ".js-businessPart-update-form", loadBusinessPartForm);
// Delete book
$("#businessPart-table").on("click", ".js-delete-businessPart", loadBusinessPartForm);
$("#modal-businessPart").on("submit", ".js-businessPart-delete-form", saveBusinessPartForm);

});
