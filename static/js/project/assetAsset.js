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
        $('.advanced2AutoComplete2').autoComplete({
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
        $('.advanced2AutoComplete2').on('autocomplete.select', function (evt, item) {
          // alert("!23");
          $("#hiddentajhiz").val(item.id);
        });
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


  var make_row=function(val){
    $.ajax({
      async: true,
      url: '/Asset/Make_Row/'+val,
      type: 'get',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          // alert("@");
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_assetAsset").empty();
          $("#tbody_assetAsset").html(data.html_assetAsset_list);
          $('.advanced2AutoComplete2').autoComplete({
            resolver: 'custom',
            noResultsText:'بدون نتیجه',
            formatResult: function (item) {
              return {
                value: item.id,
                text: "[" + item.id + "] " + item.assetName,
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
          $('.advanced2AutoComplete2').on('autocomplete.select', function (evt, item) {
            // alert("!23");
            $("#id_lastassetasset").val(item.id);
          });




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

  var addrow=function(){
    val=$("#lastAssetid").val();
    alert("");
    make_row(val);
  }

var saveAssetAsset=function(){
  child=$("#id_lastassetasset").val();
  main=$("#lastAssetid").val();
  $.ajax({
    async: true,
    url: '/Asset/Asset/create?main='+main+'&child='+child,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetAsset").empty();
        $("#tbody_assetAsset").html(data.html_assetAsset_list);
        // $('.advanced2AutoComplete2').autoComplete({
        //   resolver: 'custom',
        //   noResultsText:'بدون نتیجه',
        //   formatResult: function (item) {
        //     return {
        //       value: item.id,
        //       text: "[" + item.id + "] " + item.assetName,
        //     };
        //   },
        //   events: {
        //     search: function (qry, callback) {
        //       // let's do a custom ajax call
        //       $.ajax(
        //         '/Asset/GetAssets',
        //         {
        //           data: { 'qry': qry}
        //         }
        //       ).done(function (res) {
        //         callback(res);
        //       });
        //     },
        //   }
        // });
        // $('.advanced2AutoComplete2').on('autocomplete.select', function (evt, item) {
        //   $("#id_lastassetasset").val(item.id);
        //   console.log($("#id_lastassetasset").val());
        // });
      }
      else {

      }
    }
  });

}
var deleteAssetAsset=function(){
  $.ajax({
    async: true,
    url:  $(this).attr("data-url"),
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#tbody_assetAsset").empty();
        $("#tbody_assetAsset").html(data.html_assetAsset_list);
        // $('.advanced2AutoComplete').autoComplete({
        //   resolver: 'custom',
        //   noResultsText:'بدون نتیجه',
        //   formatResult: function (item) {
        //     return {
        //       value: item.id,
        //       text: "[" + item.id + "] " + item.assetName,
        //     };
        //   },
        //   events: {
        //     search: function (qry, callback) {
        //       // let's do a custom ajax call
        //       $.ajax(
        //         '/Asset/GetAssets',
        //         {
        //           data: { 'qry': qry}
        //         }
        //       ).done(function (res) {
        //         callback(res);
        //       });
        //     },
        //   }
        // });
        // $('.advanced2AutoComplete').on('autocomplete.select', function (evt, item) {
        //
        //
        //   $("#id_lastassetasset").val(item.id);
        //   console.log($("#id_lastassetasset").val());
        //
        //
        // });



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

 // Create book
$(".js-create-assetAsset").unbind();
$(".js-create-assetAsset").click(loadAssetAssetForm);
// $("#assetAsset-table").on("click", ".js-update-assetAsset", loadAssetAssetForm);
// $("#assetAsset-table").on("click", ".js-create-assetAsset", addrow);
$("#modal-assetAsset").on("submit", ".js-assetAsset-update-form", loadAssetAssetForm);
// Delete book
$("#assetAsset-table").on("click", ".js-delete-assetAsset", deleteAssetAsset);
$("#assetAsset-table").on("click", ".js-update-assetAsset", saveAssetAsset);
$("#modal-assetAsset").on("click", ".js-assetAsset-delete-form", deleteAssetAssetForm);

});
