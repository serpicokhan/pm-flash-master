$(function () {

  var loadStockForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-stock").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-stock .modal-content").html(data.html_stock_form);
        $(".selectpicker").selectpicker();

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
          $("#id_stockItem").val(item.id);
          $('#id_stockItem').val(item.id).trigger('change');
          // $('.basicAutoCompleteCustom').html('');
        });
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveStockForm= function () {

   var form = $(this);
   $.ajax({
     async: true,
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function()
     {
      //
     },
     success: function (data) {
       // console.log("here!");
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_stock").empty();
         $("#tbody_stock").html(data.html_stock_list);
         $("#modal-stock").modal("hide");
         toastr.success(data.html_success);
         //console.log(data.html_wo_list);
       }
       else {
         toastr.error(data.stock_err_msg);
         // console.log("what");
         // console.log(data);

         // if(data.stock_has_err=='1')
         // {
         //   toastr.error(data.stock_err_msg);
         // }
         $("#stock-table tbody").html(data.html_stock_list);
         $("#modal-stock .modal-content").html(data.html_stock_form);
       }
     },
     error:function(xxx,yyy,err){
       console.log("error");
       console.log(err);
     }
   });
   return false;
 };

 $('#option1').change(function(){

   //show all item
   $.ajax({
     url: '/Stock/ListAllItemDetails/',

     type: 'GET',
     dataType: 'json',
     success: function (data) {

       if (data.form_is_valid) {

         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_stock").empty();

         $("#tbody_stock").html(data.html_stock_list);
         $(".woPaging").html(data.html_wo_paginator);

         $("#modal-stock").modal("hide");
         $("tr").on("click",function(){
           $(".col-sm-4").show();
           $(".part_name_s").html($(this).find("td:eq(1)").text());
           // alert($(this).attr("date-url"));
           $("#selectedStockId").val($(this).attr("date-url"));
           $.ajax({
             url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetConsumes/',

             type: 'GET',
             dataType: 'json',
             success: function (data) {
               // stockpagenume+=5;

               if (data.form_is_valid) {
                 // console.log(data);
                 //alert("Company created!");  // <-- This is just a placeholder for now for testing

                 $("#vertical_timeline2").html(data.html_stock_list);
                 $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
                // console.log(data.html_amar_list);
               }
               else {


               }
             },
             error: function (jqXHR, exception) {
               alert(exception);
               console.log(exception)
             }
           });
           $.ajax({
             url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetPurchases/',

             type: 'GET',
             dataType: 'json',
             success: function (data) {
               // stockpagenume+=5;

               if (data.form_is_valid) {
                 // console.log(data);
                 //alert("Company created!");  // <-- This is just a placeholder for now for testing

                 $("#vertical_timeline1").html(data.html_stock_list);
                 $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
                // console.log(data.html_amar_list);
               }
               else {


               }
             },
             error: function (jqXHR, exception) {
               alert(exception);
               console.log(exception)
             }
           });

         }

         );
        // console.log(data.html_amar_list);
       }
       else {


       }
     },
     error: function (jqXHR, exception) {
       alert(exception);
       console.log(exception)
     }
   });
   return false;
 });
 $('#option2').change(function(){

   //show low Item
   $.ajax({
     url: '/Stock/LowItemDetails/',

     type: 'GET',
     dataType: 'json',
     success: function (data) {

       if (data.form_is_valid) {
         // console.log(data);
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_stock").empty();

         $("#tbody_stock").html(data.html_lowitemstock_list);
         $(".woPaging").html(data.html_wo_paginator);

         $("#modal-stock").modal("hide");
         $("tr").on("click",function(){
           $(".col-sm-4").show();
            $(".part_name_s").html($(this).find("td:eq(1)").text());
           // alert($(this).attr("date-url"));
           $("#selectedStockId").val($(this).attr("date-url"));
           $.ajax({
             url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetConsumes/',

             type: 'GET',
             dataType: 'json',
             success: function (data) {
               // stockpagenume+=5;

               if (data.form_is_valid) {
                 // console.log(data);
                 //alert("Company created!");  // <-- This is just a placeholder for now for testing

                 $("#vertical_timeline2").html(data.html_stock_list);
                 $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
                // console.log(data.html_amar_list);
               }
               else {


               }
             },
             error: function (jqXHR, exception) {
               alert(exception);
               console.log(exception)
             }
           });
           $.ajax({
             url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetPurchases/',

             type: 'GET',
             dataType: 'json',
             success: function (data) {
               // stockpagenume+=5;

               if (data.form_is_valid) {
                 // console.log(data);
                 //alert("Company created!");  // <-- This is just a placeholder for now for testing

                 $("#vertical_timeline1").html(data.html_stock_list);
                 $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
                // console.log(data.html_amar_list);
               }
               else {


               }
             },
             error: function (jqXHR, exception) {
               alert(exception);
               console.log(exception)
             }
           });

         }

         );
        // console.log(data.html_amar_list);
       }
       else {


       }
     },
     error: function (jqXHR, exception) {
       alert(exception);
       console.log(exception)
     }
   });
   return false;
 });
$(".selectpicker").change(function(){
  if($(this).val()==-1)
    return false;
  $.ajax({
    url: '/Stock/'+$(this).val()+'/ListGroupedStock/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_stock").empty();

        $("#tbody_stock").html(data.html_stock_list);
        $(".woPaging").html(data.html_stock_paginator);

        $("#modal-stock").modal("hide");
        $("tr").on("click",function(){
          $(".col-sm-4").show();
           $(".part_name_s").html($(this).find("td:eq(1)").text());
          // alert($(this).attr("date-url"));
          $("#selectedStockId").val($(this).attr("date-url"));
          $.ajax({
            url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetConsumes/',

            type: 'GET',
            dataType: 'json',
            success: function (data) {
              // stockpagenume+=5;

              if (data.form_is_valid) {
                // console.log(data);
                //alert("Company created!");  // <-- This is just a placeholder for now for testing

                $("#vertical_timeline2").html(data.html_stock_list);
                $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
               // console.log(data.html_amar_list);
              }
              else {


              }
            },
            error: function (jqXHR, exception) {
              alert(exception);
              console.log(exception)
            }
          });
          $.ajax({
            url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetPurchases/',

            type: 'GET',
            dataType: 'json',
            success: function (data) {
              // stockpagenume+=5;

              if (data.form_is_valid) {
                // console.log(data);
                //alert("Company created!");  // <-- This is just a placeholder for now for testing

                $("#vertical_timeline1").html(data.html_stock_list);
                $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
               // console.log(data.html_amar_list);
              }
              else {


              }
            },
            error: function (jqXHR, exception) {
              alert(exception);
              console.log(exception)
            }
          });

        }

        );
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });
  return false;

});

// //////////////////////////////////
$("tr").click(function(){
  $(".col-sm-4").show();
  $(".part_name_s").html($(this).find("td:eq(1)").text());
  // alert($(this).attr("date-url"));
  $("#selectedStockId").val($(this).attr("date-url"));
  $.ajax({
    url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetConsumes/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // stockpagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing

        $("#vertical_timeline2").html(data.html_stock_list);
        $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });
  $.ajax({
    url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetPurchases/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // stockpagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing

        $("#vertical_timeline1").html(data.html_stock_list);
        $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });

});
var searchStock=function(searchStr){
  $.ajax({
    url: '/Stock/'+searchStr+'/Search/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {

      if (data.form_is_valid) {
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_stock").empty();
        $("#tbody_stock").html(data.html_stock_list);
        $(".woPaging").html(data.html_stock_paginator);
        $("tr").on("click",function(){
          $(".col-sm-4").show();
           $(".part_name_s").html($(this).find("td:eq(1)").text());
          // alert($(this).attr("date-url"));
          $("#selectedStockId").val($(this).attr("date-url"));
          $.ajax({
            url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetConsumes/',

            type: 'GET',
            dataType: 'json',
            success: function (data) {
              // stockpagenume+=5;

              if (data.form_is_valid) {

                // console.log(data);
                //alert("Company created!");  // <-- This is just a placeholder for now for testing

                $("#vertical_timeline2").html(data.html_stock_list);
                $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
               // console.log(data.html_amar_list);
              }
              else {


              }
            },
            error: function (jqXHR, exception) {
              alert(exception);
              console.log(exception)
            }
          });
          $.ajax({
            url: '/Stock/'+$("#selectedStockId").val()+'/'+0+'/GetPurchases/',

            type: 'GET',
            dataType: 'json',
            success: function (data) {
              // stockpagenume+=5;

              if (data.form_is_valid) {
                // console.log(data);
                //alert("Company created!");  // <-- This is just a placeholder for now for testing

                $("#vertical_timeline1").html(data.html_stock_list);
                $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
               // console.log(data.html_amar_list);
              }
              else {


              }
            },
            error: function (jqXHR, exception) {
              alert(exception);
              console.log(exception)
            }
          });

        });

        // $("#modal-company").modal("hide");
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });
  return false;
} ;



$("#stockSearch").on('input',function(){
  var str=$("#stockSearch").val();
  if(str.length==0)
  str='empty_';
  str=str.replace(' ','_');
  searchStock(str);
});
//###############################################################################3
var stockpagenume=0;
var stockpurchasepagenume=0;
$("#vertical_timeline2").on('click','.woloadmore',function(){


  $.ajax({
    url: '/Stock/'+$("#selectedStockId").val()+'/'+stockpagenume+'/GetConsumes/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      stockpagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        // console.log($("#vertical_timeline2").html());
        $('#vertical_timeline2 > div').last().remove();
        $("#vertical_timeline2").append(data.html_stock_list);
        $("#vertical_timeline2").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width woloadmore">بیشتر</button>                </div>              </div>          </div>');
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });
  return false;

});
$("#vertical_timeline1").on('click','.purchaseloadmore',function(){


  $.ajax({
    url: '/Stock/'+$("#selectedStockId").val()+'/'+stockpagenume+'/GetPurchases/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {
      stockpurchasepagenume+=5;

      if (data.form_is_valid) {
        // console.log(data);
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        // console.log($("#vertical_timeline2").html());
        $('#vertical_timeline1 > div').last().remove();
        $("#vertical_timeline1").append(data.html_stock_list);
        $("#vertical_timeline1").append('    <div class="vertical-timeline-block">                            <div class="vertical-timeline-content">                <div class="text-center">                  <button type="button" class="btn btn-info block full-width purchaseloadmore">بیشتر</button>                </div>              </div>          </div>');
       // console.log(data.html_amar_list);
      }
      else {


      }
    },
    error: function (jqXHR, exception) {
      alert(exception);
      console.log(exception)
    }
  });
  return false;

});
////////////////////////////////////////////
 // Create book
$(".js-create-stock").click(loadStockForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#stock-table").on("click", ".js-update-stock", loadStockForm);

$("#modal-stock").on("submit", ".js-stock-update-form", loadStockForm);
// Delete book
$("#stock-table").on("click", ".js-delete-stock", loadStockForm);
$("#modal-stock").on("submit", ".js-stock-delete-form", saveStockForm);

});
