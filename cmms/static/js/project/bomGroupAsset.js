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

        //new form2
        $(".main_assets1").html(data.main_assets);
        //end of new form2

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
          $("#id_BOMGroupAssetAsset").val(item.id);
          $('#id_BOMGroupAssetAsset').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};
var change_makan=function(){
  makan=$("#id_makan").val()||-1;
  assetType=$("#id_assetType").val()||-1;
  srch=$("#assetSearch").val()||-1;
  $.ajax({
    url: '/BOMGroupAsset/SelectAsset?makan='+makan+'&assettype='+assetType+'&srch='+srch,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $("#tbody_bomgroupasset2").html(data.html);
      $(".assetPaging").html(data.page);
    }
  });
  // save_check();

}
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


var save_check=function(){
  storeSelected();
}
const selectedValues = [];
const storeSelected = () => {
  console.log(selectedValues );
  const checkboxes = document.querySelectorAll('.selection-box');


  checkboxes.forEach(checkbox => {
    const value = checkbox.value;
   const index = selectedValues.indexOf(value);
    if (checkbox.checked) {
    if (index === -1) {
      selectedValues.push(value);

    }
  } else {
    if (index !== -1) {
      selectedValues.splice(index, 1);
    }
  }
  });
  $("#assetNamesHidden").val(selectedValues);

  // Store the selected values in your desired location (e.g., array, variable, etc.)
  // return selectedValues;
};
var loadAssetPage=function(){
  var mydata=$(this).attr('data-url');
  $.ajax({
    url: '/BOMGroupAsset/AssetPage'+mydata,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $("#tbody_bomgroupasset2").html(data.html);
      $(".assetPaging").html(data.page);
    }
  });
}
 // Create book
// $(".js-create-bomGroupAsset").unbind();
// $(".js-create-bomGroupAsset").click(loadBOMGroupAssetForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#modal-company").on("click", ".js-update-bomGroupAsset", loadBOMGroupAssetForm);
$("#modal-company").on("click", ".js-create-bomGroupAsset", loadBOMGroupAssetForm);
$("#modal-bomGroupAsset").on("click", "#pnextasset", loadAssetPage);
$("#modal-bomGroupAsset").on("click", "#pprevasset", loadAssetPage);

$("#modal-bomGroupAsset").on("submit", ".js-bomGroupAsset-update-form", loadBOMGroupAssetForm);
// Delete book
$("#modal-company").on("click", ".js-delete-bomGroupAsset", loadBOMGroupAssetForm);
$("#modal-bomGroupAsset").on("submit", ".js-bomGroupAsset-delete-form", saveBOMGroupAssetForm);
$("#modal-bomGroupAsset").on("click", ".js-bomGroupAsset-delete-form", deleteBOMGroupAssetForm);
$("#modal-company").on("change", ".js-bomGroupAsset-list", change_makan);
$("#modal-company").on("input", "#assetSearch", change_makan);
$("#modal-company").on("change", ".selection-box", save_check);




});
