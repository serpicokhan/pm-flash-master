$(function(){


 var showLocationSelector=function(){


      $.ajax({
       url: '/Asset/Location/Category',
       beforeSend: function () {

         $("#modal-assetcategory").modal({backdrop: 'static', keyboard: false});
       },
       success: function (data) {

         //data.modalassetcat
          $("#modal-assetcategory .modal-content").html(data.modalassetcat);
       }
     });


 }
 var showPartSelector=function(){


   $('.partselector').autoComplete({
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
   $('.partselector').on('autocomplete.select', function (evt, item) {
     $("#id_part").val(item.id);
     $('#id_part').val(item.id).trigger('change');
     // $('.basicAutoCompleteCustom').html('');
   });


 }
 $("#modal-simplereport").on("click",".assetselector",showLocationSelector);
 $("#modal-simplereport").on("click",".partselector",showPartSelector);
});
