$(function () {

  var loadBOMGroupPartForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-bomGroupPart").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-bomGroupPart .modal-content").html(data.html_bomGroupPart_form);
        $('.advanced2AutoComplete').autoComplete({
          resolver: 'custom',
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.partCode + "] " + item.partName,

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
          $("#id_BOMGroupPartPart").val(item.id);
          $('#id_BOMGroupPartPart').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveBOMGroupPartForm= function () {

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
 var deleteBOMGroupPartForm= function (event) {
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
          $("#tbody_bomGroupPart").empty();
          $("#tbody_bomGroupPart").html(data.html_bomGroupPart_list);
          $('#modal-bomGroupPart').modal('hide');

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
  var change_part_type=function(){
    partcategory=$("#id_partCategory").val()||-1;
    srch=$("#partSearch").val()||-1;
    $.ajax({
      url: '/BOMGroupPart/SelectPart?pcategory='+partcategory+'&srch='+srch,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        $("#tbody_bomgrouppart2").html(data.html);
        $(".woPaging").html(data.page);
      }
    });
    // save_check();

  }
  var save_part_check=function(){
    storePartSelected();
  }
  const selectedPartValues = [];
  const storePartSelected = () => {
    const checkboxes = document.querySelectorAll('.selection-box');


    checkboxes.forEach(checkbox => {
      const value = checkbox.value;
     const index = selectedValues.indexOf(value);
      if (checkbox.checked) {
      if (index === -1) {
        selectedPartValues.push(value);

      }
    } else {
      if (index !== -1) {
        selectedPartValues.splice(index, 1);
      }
    }
    });
    $("#partNamesHidden").val(selectedPartValues);

    // Store the selected values in your desired location (e.g., array, variable, etc.)
    // return selectedValues;
  };
 // Create book
// $(".js-create-bomGroupPart").click(loadBOMGroupPartForm);
//$d("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
var loadPartPage=function(){
  var mydata=$(this).attr('data-url');

  $.ajax({
    url: '/BOMGroupPart/SelectPartPage'+mydata,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $("#tbody_bomgrouppart2").html(data.html);
      $(".woPaging").html(data.page);
    }
  });

}
// Update book
$("#bomGroupPart-table").on("click", ".js-update-bomGroupPart", loadBOMGroupPartForm);

$("#modal-bomGroupPart").on("submit", ".js-bomGroupPart-update-form", loadBOMGroupPartForm);
$("#modal-company").on("click", ".js-create-bomGroupPart", loadBOMGroupPartForm);
// Delete book
$("#bomGroupPart-table").on("click", ".js-delete-bomGroupPart", loadBOMGroupPartForm);
$("#modal-bomGroupPart").on("submit", ".js-bomGroupPart-delete-form", saveBOMGroupPartForm);
$("#modal-bomGroupPart").on("click", "#ppprev", loadPartPage);
$("#modal-bomGroupPart").on("click", "#ppnext", loadPartPage);
$("#modal-bomGroupPart").on("click", ".js-bomGroupPart-delete-form", deleteBOMGroupPartForm);
$("#modal-bomGroupPart").on("change", ".js-bomGroupPart-change", change_part_type);
$("#modal-bomGroupPart").on("input", "#partSearch", change_part_type);
});
