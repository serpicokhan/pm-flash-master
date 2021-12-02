$(function () {

  var loadAssetAssetForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetAsset").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-assetAsset .modal-content").html(data.html_assetAsset_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetAssetForm= function () {

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
         $("#tbody_assetAsset").empty();
         $("#tbody_assetAsset").html(data.html_assetAsset_list);
         $("#modal-assetAsset").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#assetAsset-table tbody").html(data.html_assetAsset_list);
         $("#modal-assetAsset .modal-content").html(data.html_assetAsset_form);
       }
     }
   });
   return false;
 };
 var deleteAssetAssetForm= function (event) {
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
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_assetAsset").empty();
          $("#tbody_assetAsset").html(data.html_assetAsset_list);
          $('#modal-assetAsset').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {
          //
          // $("#task-table tbody").html(data.html_task_list);
          // $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };
  var addrow=function(){
    var i=0;
    $('#assetAsset-table').append('<tr><td><input class="form-control advanced2AutoComplete"/></td><td>Record2</td></tr>');
    $('.advanced2AutoComplete').autoComplete({
      resolver: 'custom',
      noResultsText:'بدون نتیجه',
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
  }



 // Create book
$(".js-create-assetAsset").unbind();
$(".js-create-assetAsset").click(addrow);
$("#assetAsset-table").on("click", ".js-update-assetAsset", loadAssetAssetForm);
// $("#assetAsset-table").on("click", ".js-create-assetAsset", addrow);
$("#modal-assetAsset").on("submit", ".js-assetAsset-update-form", loadAssetAssetForm);
// Delete book
$("#assetAsset-table").on("click", ".js-delete-assetAsset", loadAssetAssetForm);
$("#modal-assetAsset").on("click", ".js-assetAsset-delete-form", deleteAssetAssetForm);

});
