$(function () {
  ///////////////////////////////////////////////

  const urlParams = new URLSearchParams(window.location.search);

  // Read individual query parameters
  const param1 = urlParams.get('dttextFrom'); // "value1"
  const param2 = urlParams.get('dttextTo'); // "value2"
  const param3 = urlParams.get('makan'); // "value2"
  $("#id_makan").val(param3);
  $('#dttextFrom').pDatepicker({
    format: 'YYYY-MM-DD',
    autoClose: true,
    initialValueType: 'gregorian'
  }).val(param1);
  $('#dttextTo').pDatepicker({
    format: 'YYYY-MM-DD',
    autoClose: true,
    initialValueType: 'gregorian'
  }).val(param2);
var filterAssetLife=function(){
  makan=$("#id_makan").val()||0;
  window.location='/AssetLife?dttextFrom='+$("#dttextFrom").val()+'&dttextTo='+$("#dttextTo").val()+'&makan='+makan;
}
  var loadAssetLifeForm =function () {
    var btn=$(this);
    // console.log(btn.attr("data-url"));
// console.log(1);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-assetLife").modal({backdrop: 'static', keyboard: false});
        $('#modal-assetLife').data('bs.modal').options.backdrop = 'static';
      },
      success: function (data) {

        $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
        $(".selectpicker").selectpicker();

        // ############

        $('.advanced2AutoComplete4').autoComplete({
          resolver: 'custom',
          noResultsText:'بدون نتیجه',
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
                callback(res);
              });
            },
          }
        });
        $('.advanced2AutoComplete4').on('autocomplete.select', function (evt, item) {
          // alert("!23");
        $("#id_assetLifeAssetid").val(item.id);
        });
        // ##############




        $('#id_assetOfflineFrom').pDatepicker({
          format: 'YYYY-MM-DD',
          autoClose: true,
          initialValueType: 'gregorian'

            });
        $('#id_assetOnlineFrom').pDatepicker({
          format: 'YYYY-MM-DD',
          autoClose: true,
          initialValueType: 'gregorian'
                                              });

    $('.selectpicker').selectpicker();
    $('.woselector').autoComplete({
      resolver: 'custom',
      minLength:1,
      formatResult: function (item) {
        return {
          value: item.id,
          text: "[" + item.id + "] " + item.summaryofIssue,

        };
      },
      events: {
        search: function (qry, callback) {
          // let's do a custom ajax call
          $.ajax(
            '/WorkOrder/GetWos',
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
    $('.woselector').on('autocomplete.select', function (evt, item) {
      $("#id_assetWOAssoc").val(item.id);
      $('#id_assetWOAssoc').val(item.id).trigger('change');
      // $('.basicAutoCompleteCustom').html('');
    });


      }//end success
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveAssetLifeForm= function () {

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
         $("#tbody_assetLife").empty();
         $("#tbody_assetLife").html(data.html_assetLife_list);
         $("#modal-assetLife").modal("hide");

         //console.log(data.html_wo_list);
       }
       else {

         $("#assetLife-table tbody").html(data.html_assetLife_list);
         $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
       }
     }
   });
   return false;
 };
 var deleteAssetLifeForm= function (event) {
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
          $("#tbody_assetLife").empty();
          $("#tbody_assetLife").html(data.html_assetLife_list);
          $("#modal-assetLife").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#assetLife-table tbody").html(data.html_assetLife_list);
          $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
        }
      }
    });
  }
    return false;
  };

 // Create book
$(".js-create-assetLife").unbind();
$(".js-create-assetLife").click(loadAssetLifeForm);
$("#btnfilter").click(filterAssetLife);
$("#assetLife-table").on("click", ".js-update-assetLife", loadAssetLifeForm);

$("#modal-assetLife").on("submit", ".js-assetLife-update-form", loadAssetLifeForm);
// Delete book
$("#assetLife-table").on("click", ".js-delete-assetLife", loadAssetLifeForm);
$("#modal-assetLife").on("click", ".js-assetLife-delete-form", deleteAssetLifeForm);

});
