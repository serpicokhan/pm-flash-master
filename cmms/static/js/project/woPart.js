$(function () {


  var loadWoPartForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-woPart").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        $("#modal-woPart .modal-content").html(data.html_woPart_form);
      //   $("#id_woPartPart").change(function(){
      //
      //   $.ajax({
      //     async: true,
      //     url: '/WoPart/'+$('#id_woPartPart').val()+'/GetPartStock/',
      //     type: 'get',
      //     dataType: 'json',
      //     success: function (data) {
      //       console.log(data);
      //       // $("#id_woPartStock").html(data.result.result);
      //       // $('.selectpicker').selectpicker('render');
      //       // $('.selectpicker').selectpicker('refresh');
      //
      //
      //     }
      //   });
      // });

        // $('.selectpicker').selectpicker();
        $('.advanced2AutoComplete').autoComplete({
					resolver: 'custom',
          minChars:1,
					formatResult: function (item) {
						return {
							value: item.id,
							text: "[" + item.id + "] " + item.stockItem__partName,

						};
					},
					events: {
						search: function (qry, callback) {
							// let's do a custom ajax call
							$.ajax(
								'/WoPart/GetStockParts',
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
          console.log("here",item);
					$("#id_woPartStock").val(item.id);
          $('#id_woPartStock').val(item.id).trigger('change');
          console.log($('#id_woPartStock').val());
					// $('.basicAutoCompleteCustom').html('');
				});

        // $('.basicAutoComplete').autoComplete(set,{ value: id});
      }
    });
};



 var deleteWoPartForm= function (event) {

    var form = $(this);

    if(event.target.className=="btn btn-danger")
    {
    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_woPart").empty();
          $("#tbody_woPart").html(data.html_woPart_list);
          $("#modal-woPart").modal("hide");

          //console.log(data.html_wo_list);
        }
        else {

          $("#woPart-table tbody").html(data.html_woPart_list);
          $("#modal-woPart .modal-content").html(data.html_woPart_form);
        }
      }
    });
  }
    return false;
  };

var LoadStockForm=function(){
   // $("#modal-woPartStock").modal("show");
   var btn = $('<button/>',
     {
         text: 'Test',
         'data-url':'/Stock/listStockModal/',
         click: function () { alert('hi'); },

     });
   $.ajax({
     url: btn.attr("data-url"),
     type: 'get',
       async: true,
     dataType: 'json',
     beforeSend: function () {
       //alert(btn.attr("data-url"));
       $("#modal-woPartStock").modal('show');
     },
     success: function (data) {
       // console.log(data);
       $("#modal-woPartStock .modal-content").html(data.html_stock_list);


       // $('.selectpicker').selectpicker();

      }
    });





};
var LoadStockNewForm=function(){
   // $("#modal-woPartStock").modal("show");
   var btn = $('<button/>',
     {
         text: 'Test',
         'data-url':'/Stock/create2/',
         click: function () { alert('hi'); },

     });
   $.ajax({
     url: btn.attr("data-url"),
     type: 'get',
       async: true,
     dataType: 'json',
     beforeSend: function () {
       //alert(btn.attr("data-url"));
       $("#modal-woPartStockNew").modal('show');
     },
     success: function (data) {
       // console.log(data);
       $("#modal-woPartStockNew .modal-content").html(data.html_stock_form);
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
             // alert(1);
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
         console.log("here Start");
         console.log(item);
         $("#id_stockItem").val(item.id);
         $('#id_stockItem').val(item.id).trigger('change');
         // $('.basicAutoCompleteCustom').html('');
       });


       // $('.selectpicker').selectpicker();

      }
    });





};
var LoadPartNewForm=function(){
   // $("#modal-woPartStock").modal("show");
   var btn = $('<button/>',
     {
         text: 'Test',
         'data-url':'/Part/create2/',
         click: function () { alert('hi'); },

     });
   $.ajax({
     url: btn.attr("data-url"),
     type: 'get',
       async: true,
     dataType: 'json',
     beforeSend: function () {
       //alert(btn.attr("data-url"));
       $("#modal-woPartPartNew").modal('show');
     },
     success: function (data) {
       // console.log(data);
       $("#modal-woPartPartNew .modal-content").html(data.html_part_form);


       // $('.selectpicker').selectpicker();

      }
    });





};
var searchStock=function(searchStr){
  $.ajax({
    url: '/Stock/'+searchStr+'/Search2/',

    type: 'GET',
    dataType: 'json',
    success: function (data) {

      if (data.form_is_valid) {
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_stock").empty();
        $("#tbody_stock").html(data.html_stock_list);
        // $(".woPaging").html(data.html_stock_paginator);


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
var stSearch=function(){
  var str=$("#stockSearch").val();
  if(str.length==0)
  str='empty_';
  str=str.replace(' ','_');
  searchStock(str);
};
var selectStockItem=function(){


  $("#id_mypart").val($(this).attr("data-name"));
  $("#id_woPartStock").val($(this).attr("data-url"));
  $("#modal-woPartStock").modal("hide");

}
 // Create book
$(".js-create-woPart").unbind();
$(".js-create-woPart").click(loadWoPartForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#woPart-table").on("click", ".js-update-woPart", loadWoPartForm);

$("#modal-woPart").on("submit", ".js-woPart-update-form", loadWoPartForm);
// Delete book
$("#woPart-table").on("click", ".js-delete-woPart", loadWoPartForm);
$("#modal-woPart").on("click", ".js-woPart-delete-form", deleteWoPartForm);
$("#modal-woPart").on("click", ".js-woPartStock-create-form", LoadStockForm);
  $("#modal-woPartStock").on("click", ".js-add-new-stock-modal",LoadStockNewForm);
  $("#modal-woPartStock").on("keyup", ".stockSearch",stSearch);
  $("#modal-woPartStockNew").on("click", ".js-add-new-part",LoadPartNewForm);
  $("#modal-woPartStock").on("click", ".js-select-stock",selectStockItem);

});
