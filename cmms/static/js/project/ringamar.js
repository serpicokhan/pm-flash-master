var firstPressedButton = null;
// var isCtrlPressed = false;
// var selectedCells = [];
//
//     $(document).keydown(function(event) {
//       if (event.which === 17) { // 17 is the key code for Control (Ctrl)
//         isCtrlPressed = true;
//       }
//     });
//
//     $(document).keyup(function(event) {
//       if (event.which === 17) { // 17 is the key code for Control (Ctrl)
//         isCtrlPressed = false;
//       }
//     });
//
//         // Event delegation for cell click event
//         $('#company-table').on('click', 'td[contenteditable="true"]', function(event) {
//           if (isCtrlPressed) {
//             $(this).toggleClass('selected');
//
//             var cellValue = $(this).html();
//             var cellIndex = $(this).index();
//             var rowIndex = $(this).closest('tr').index();
//             var cellKey = rowIndex + '-' + cellIndex;
//
//             if ($(this).hasClass('selected')) {
//               selectedCells[cellKey] = cellValue;
//             } else {
//               delete selectedCells[cellKey];
//             }
//           }
//         });
//
//         // Event delegation for cell blur event
//         $('#company-table').on('blur', 'td[contenteditable="true"]', function(event) {
//           if (isCtrlPressed) {
//             var newValue = $(this).html();
//             for (var cellKey in selectedCells) {
//               var cell = $('#' + cellKey);
//               cell.html(newValue);
//             }
//           }
//         });

$(function () {

  var senddata=function(){
    var data = [];
        $('#company-table tr').each(function() {
          var id=$(this).attr('data-id');
          var radif = $(this).find('td:eq(0)').text()||0;
          var assetAmarDate = $(this).find('td:eq(1)').attr('data-date')||0;
          var assetName = $(this).find('td:eq(2)').attr('data-assetname')||0;
          var shift = $(this).find('td:eq(3)').text()||0;
          var assetStartKilometer = $(this).find('td:eq(4)').text()||0;
          var assetEndKilometer = $(this).find('td:eq(5)').text()||0;
          var assetTotlaKilometer = $(this).find('td:eq(6)').text()||0;
          var assetStartTime = $(this).find('td:eq(7)').text()||0;
          var assetEndTime = $(this).find('td:eq(8)').text()||0;
          var assetTotalTime = $(this).find('td:eq(9)').text()||0;
          var operatorName = $(this).find('td:eq(10)').text()||'';
          var assetDaf = $(this).find('td:eq(11)').text()||0;
          data.push({ id: id, radif: radif,assetAmarDate: assetAmarDate, assetName: assetName,ShiftTypes: shift
            , assetStartKilometer: assetStartKilometer,assetEndKilometer: assetEndKilometer, assetTotlaKilometer: assetTotlaKilometer
            ,assetStartTime: assetStartTime, assetEndTime: assetEndTime, assetTotalTime: assetTotalTime, operatorName: operatorName, assetDaf: assetDaf });
        });
        console.log(JSON.stringify(data));

    $.ajax({
      url: '/RingAmar/SaveTableInfo',
         method: 'POST',
         data: JSON.stringify(data),
         contentType: 'application/json',
         success: function(response) {
           // Handle the response from the server
           console.log('Data sent successfully');
           toastr.success("اطلاعات با موفقیت ارسال شد");
         },
         error: function(xhr, status, error) {
           // Handle the error
            toastr.success("خطا در ارسال داده ها");
           console.log('Error sending data:', error);
         }
    });
  }
  $("#btncreate").click(function(){
    $.ajax({
      url: '/RingAmar/LoadTableInfo?cat=17&makan='+mak_val+'&dt='+$("#dttext").val()+'&shift='+$("#shift").val(),
      type: 'get',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
        $("#tbody_amar").html('');
        $("#tbody_amar").html(data.amar);
        }
        else {

        toastr.error("خطایی بوجود آمده لطفا مجددا سعی نمایید");
        }
      }
    });
  });
  $('#dttext').pDatepicker({
    format: 'YYYY-MM-DD',
    autoClose: true,
    initialValueType: 'gregorian'
  });
  var loadForm =function (btn1) {
    var btn=0;
    //console.log(btn1);
    if($(btn1).attr("type")=="click")
     btn=$(this);
    else {
      btn=btn1;
    }
    //console.log($(btn).attr("type"));
    // console.log(btn.attr("data-url")+'?q='+$("#id_assetName").val());
    return $.ajax({
      url: btn.attr("data-url")+'?q='+$("#id_makan").val(),
      type: 'get',
      dataType: 'json',
      beforeSend: function (xhr,x) {
        if($("#id_assetName").val()=== null ||$("#id_assetName").val()==='' ){
          toastr.error("مکان را انتخاب نمایید");
          xhr.abort();
          return;
        }

        $("#modal-company").modal("show");

      },
      success: function (data) {
        $("#modal-company .modal-content").html(data.html_ringAmar_form);
        $('#id_assetAmarDate').pDatepicker({
          format: 'YYYY-MM-DD',
          autoClose: true,
          initialValueType: 'gregorian'
        });


      }
    });



};
// $('#company-table').on('focus', '.advanced2AutoComplete', function() {
//   $('advanced2AutoComplete').autoComplete({
//     resolver: 'custom',
//     minChars:1,
//     formatResult: function (item) {
//       return {
//         value: item.operatorName,
//         text:  item.operatorName,
//
//       };
//     },
//     events: {
//       search: function (qry, callback) {
//         // let's do a custom ajax call
//         $.ajax(
//           '/RingAmar/GetOpName',
//           {
//             data: { 'qry': qry}
//           }
//         ).done(function (res) {
//           console.log(res);
//           callback(res)
//         });
//       },
//
//     }
//   });
//   $('.advanced2AutoComplete').on('autocomplete.select', function (evt, item) {
//     console.log("here",item);
//     $(this).val(item.operatorName);
//     $(this).val(item.operatorName).trigger('change');
//     // console.log($('#id_woPartStock').val());
//     // $('.basicAutoCompleteCustom').html('');
//   });
//     });

//$("#modal-company").on("submit", ".js-company-create-form",
var saveForm= function () {
   var form = $(this);
   console.log(form.serialize());

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     errors:function(x,y,z){
       console.log(x);
       console.log(y);
       console.log(z);
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_ringAmar_list);
         $("#modal-company").modal("hide");
        // console.log(data.html_ringAmar_list);
       }
       else {

         $("#company-table tbody").html(data.html_ringAmar_list);
         $("#modal-company .modal-content").html(data.html_ringAmar_form);
       }
     }
   });
   return false;
 };
var applyForm= function () {

   var form = $("#amarform");
   console.log(form.serialize());

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     errors:function(x,y,z){
       console.log(x);
       console.log(y);
       console.log(z);
     },
     success: function (data) {
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_ringAmar_list);
         toastr.success("اطلاعات با موفقت درج شد");
         $("input[type=text][name!=assetAmarDate], textarea").val("");
         $("input[type=number], textarea").val("0");


        // console.log(data.html_ringAmar_list);
       }
       else {
         toastr.error("ورودیهای خود را مجدد چک کنید");

       }
     }
   });
   return false;
 };




 var myWoLoader= function(){
   btn=$(this);



   //$.when(loadForm(btn)).done(initLoad,initWoRingAmarLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad);
   //$.when(loadForm(btn)).done(initRingAmarFileLoad,initRingAmarAssetLoad,initRingAmarPartLoad );
   loadForm(btn);

   //initLoad();
 }
var loadkilometer=function(){
  if(  $("#id_assetStartKilometer").val()===null ||   $("#id_assetStartKilometer").val()==0){
  $.ajax({
    url: '/RingAmar/GetMax/?asset_id='+$("#id_assetName").val()+'&shift='+$("#id_ShiftTypes").val()+'&date='+$("#id_assetAmarDate").val(),

    type: 'get',
    dataType: 'json',
    errors:function(x,y,z){
      console.log(x);
      console.log(y);
      console.log(z);
    },
    success: function (data) {
      console.log(data);
      $("#id_assetStartKilometer").val(data.x);
    }
  });
}
}
var loadTime=function(){
  $.ajax({
    url: '/RingAmar/GetMaxTime/?asset_id='+$("#id_assetName").val()+'&shift='+$("#id_ShiftTypes").val()+'&date='+$("#id_assetAmarDate").val(),

    type: 'get',
    dataType: 'json',
    errors:function(x,y,z){
      console.log(x);
      console.log(y);
      console.log(z);
    },
    success: function (data) {
      console.log(data);
      $("#id_assetStartTime").val(data.x);
    }
  });
}

var subkilometer=function(){
  var x1=$("#id_assetStartKilometer").val();
  var x2=$("#id_assetEndKilometer").val();
  // console.log(x1,x2);
  var x3=x2-x1;
  // console.log(x3);
  $("#id_assetTotlaKilometer").val(Math.abs(x3));
}
var subTime=function(){
  var x1=$("#id_assetStartTime").val();
  var x2=$("#id_assetEndTime").val();
  // console.log(x1,x2);
  var x3=x2-x1;
  // console.log(x3);
  $("#id_assetTotalTime").val(Math.abs(x3));
}




$('#company-table').on('focusout', '.stk, .endk', function() {
        var row = $(this).closest('tr');
        var column1Value = parseFloat(row.find('.stk').text()) || 0;
        var column2Value = parseFloat(row.find('.endk').text()) || 0;
        var result = Math.abs(column1Value - column2Value);

        row.find('.totalk').text(result.toFixed(2));
      });
$('#company-table').on('focus', '.stk', function() {
        var row = $(this).closest('tr');
        var id=row.attr('data-id')
        var col1 = row.find('.stk');
        var shift = row.find('.shift').text();
        var assetname = row.find('.assetname').attr('data-assetname');
        // var column2Value = parseFloat(row.find('.endk').text()) || 0;
        // var result = Math.abs(column1Value - column2Value);
        //
        // row.find('.totalk').text(result.toFixed(2));
        // var cell=row.find('.totalk').text(result.toFixed(2));
        if(  col1.text()===null ||   col1.text()==0){
        $.ajax({
          url: '/RingAmar/GetMax/?asset_id='+assetname+'&shift='+shift,//+'&date='+$("#id_assetAmarDate").val(),

          type: 'get',
          dataType: 'json',
          errors:function(x,y,z){
            console.log(x);
            console.log(y);
            console.log(z);
          },
          success: function (data) {
            console.log(data);
            col1.text(data.x);
          }
        });
      }
      });
$('#company-table').on('focus', '.stt', function() {
        var row = $(this).closest('tr');
        var id=row.attr('data-id')
        var col1 = row.find('.stt');
        var shift = row.find('.shift').text();
        var assetname = row.find('.assetname').attr('data-assetname');
        // var column2Value = parseFloat(row.find('.endk').text()) || 0;
        // var result = Math.abs(column1Value - column2Value);
        //
        // row.find('.totalk').text(result.toFixed(2));
        // var cell=row.find('.totalk').text(result.toFixed(2));
        if(  col1.text()===null ||   col1.text()==0){
          $.ajax({
            url: '/RingAmar/GetMaxTime/?asset_id='+assetname+'&shift='+shift,//+'&date='+$("#id_assetAmarDate").val(),

            type: 'get',
            dataType: 'json',
            errors:function(x,y,z){
              console.log(x);
              console.log(y);
              console.log(z);
            },
            success: function (data) {
              console.log(data);
              col1.text(data.x);
            }
          });
      }
      });
$('#company-table').on('focusout', '.stt, .endt', function() {
        var row = $(this).closest('tr');
        if($("#id_makan").val()!=6961){
          var column1Value = parseFloat(row.find('.stt').text()) || 0;
          var column2Value = parseFloat(row.find('.endt').text()) || 0;

          var result = Math.abs(column1Value - column2Value);
          row.find('.totalt').text(result.toFixed(2));

        }
        else{
          console.log("line 4");
          var col1 = parseFloat(row.find('.totalk').text()) || 0;

          var x=Math.floor(col1/180);
          var x1=Math.floor(x/3);
          console.log(col1,x,x1);
          row.find('.totalt').text(parseFloat(x.toString()+'.'+x1.toString()));


        }




      });
$('#company-table').on('keydown', '.editable-cell', function(e) {
       var keyCode = e.keyCode || e.which;

       if (keyCode === 13) { // Enter key
         e.preventDefault();

         // Find the current cell and its parent row
         var currentCell = $(this);
         var currentRow = currentCell.closest('tr');

         // Find the next row and the corresponding cell in the same column
         var nextRow = currentRow.next('tr');
         var nextCell = nextRow.find('td:eq(' + currentCell.index() + ')');

         if (nextCell.length > 0) {
           nextCell.focus();
         } else {
           // If there is no next cell in the same column, move to the first cell of the next row
           nextRow = currentRow.next('tr');
           nextCell = nextRow.find('td:eq(0)');
           if (nextCell.length > 0) {
             nextCell.focus();
           }
         }
       }
     });

var load_assetlife=function(){
  var row = $(this).closest('tr');
  var asset_id= parseInt(row.find('.assetname').attr('data-assetname')) || 0;
  // console.log(asset_id);
  firstPressedButton=$(this);
  // localStorage.setItem('myData', $(this));
  console.log($(this));
  js_switch_change(asset_id);
}
var js_switch_change=function(asset_id)
{


  $.ajax({
    url: '/AssetLife/'+asset_id+'/eval/?stdate='+$("#dttext").val(),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-assetLife").modal({backdrop: 'static', keyboard: false});
      // $('#modal-assetLife').data('bs.modal').options.backdrop = 'static';
    },
    success: function (data) {



      tab="tab-assetlife"

       $('.nav-tabs a[href="#' + tab + '"]').tab('show');

      $("#modal-assetLife .modal-content").html(data.html_assetLife_form);
      // if($("#id_assetStatus").is(":checked")==true)
      // {
      //   $('.nav-tabs a[href="#' + 'tab-correct' + '"]').tab('show');
      // }
      // else {
      //   $('.nav-tabs a[href="#' + 'tab-failur' + '"]').tab('show');
      // }

      $('#id_assetOfflineFrom').pDatepicker({
                              format: 'YYYY-MM-DD',

            autoClose: true,
            // onSelect:function(unix){
            //   assetOfflineFrom=new Date(unix);
            // }
          });
      $('#id_assetOnlineFrom').pDatepicker({
                                  format: 'YYYY-MM-DD',

                autoClose: true,
                // onSelect: function(unix){
                //
                //  // var date1 = new Date(Date.parse($("#id_assetOfflineFrom").attr("value")));
                //   // var date2 = new Date(Date.parse($("#id_assetOnlineFrom").attr("value")));
                //   assetLifeOnlineFrom=new Date(unix);
                //   // var timeDiff = Math.abs(assetLifeOnlineFrom.getTime() - assetLifeOfflineFrom.getTime());
                //   // var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                //   // alert(diffDays);
                // }
                                            });
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





      if($("#id_assetStatus").is(":checked")==true)
      {
        $('.nav-tabs a[href="#' + 'tab-correct' + '"]').tab('show');
      }
      else {
        $('.nav-tabs a[href="#' + 'tab-failur' + '"]').tab('show');
      }
      //console.log(data.html_assetLife_form)
    },
    error:function(x,y,z)
    {
      // alert("123");
    }
  });
}

$(".js-create-ringAmar").click(myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-create-form", saveForm);

// Update book
$('#company-table').on('focus', 'td[contenteditable="true"]', function() {
     selectText(this);
   });

   function selectText(element) {
     var range = document.createRange();
     range.selectNodeContents(element);

     var selection = window.getSelection();
     selection.removeAllRanges();
     selection.addRange(range);
   }
$("#company-table").on("click", ".js-update-ringAmar", myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-update-form", saveForm);
$("#modal-company").on("focus", "#id_assetStartKilometer", loadkilometer);
// $("#modal-company").on("focus", "#id_assetStartTime", loadTime);
$("#modal-company").on("focus", "#id_assetTotlaKilometer", subkilometer);
$("#modal-company").on("focus", "#id_assetTotalTime", subTime);
$("#modal-company").on("click", ".create-next", applyForm);
// Delete book
$("#company-table").on("click", ".js-delete-ringAmar", loadForm);
$("#company-table").on("click", ".js-create-tavaghof", load_assetlife);
$(".savetableinfo").on("click", senddata);
$("#modal-company").on("submit", ".js-ringAmar-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
