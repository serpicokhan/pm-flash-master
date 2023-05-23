
$(function () {

  var senddata=function(){
    var data = [];
        $('#company-table tr').each(function() {
          var id=$(this).attr('data-id');
          var radif = $(this).find('td:eq(0)').text();
          var assetAmarDate = $(this).find('td:eq(1)').attr('data-date');
          var assetName = $(this).find('td:eq(2)').attr('data-assetname');
          var shift = $(this).find('td:eq(3)').text();
          var assetStartKilometer = $(this).find('td:eq(4)').text();
          var assetEndKilometer = $(this).find('td:eq(5)').text();
          var assetTotlaKilometer = $(this).find('td:eq(6)').text();
          var assetStartTime = $(this).find('td:eq(7)').text();
          var assetEndTime = $(this).find('td:eq(8)').text();
          var assetTotalTime = $(this).find('td:eq(9)').text();
          var operatorName = $(this).find('td:eq(10)').text();
          var assetDaf = $(this).find('td:eq(11)').text();
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
         },
         error: function(xhr, status, error) {
           // Handle the error
           console.log('Error sending data:', error);
         }
    });
  }
  $("#btncreate").click(function(){
    $.ajax({
      url: '/RingAmar/LoadTableInfo?makan='+mak_val+'&dt='+$("#dttext").val()+'&shift='+$("#shift").val(),
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
        $('.advanced2AutoComplete').autoComplete({
					resolver: 'custom',
          minChars:1,
					formatResult: function (item) {
						return {
							value: item.operatorName,
							text:  item.operatorName,

						};
					},
					events: {
						search: function (qry, callback) {
							// let's do a custom ajax call
							$.ajax(
								'/RingAmar/GetOpName',
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
					$("#id_operatorName").val(item.operatorName);
          $('#id_operatorName').val(item.operatorName).trigger('change');
          // console.log($('#id_woPartStock').val());
					// $('.basicAutoCompleteCustom').html('');
				});

      }
    });



};
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
$(".js-create-ringAmar").click(myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-ringAmar", myWoLoader);
$("#modal-company").on("submit", ".js-ringAmar-update-form", saveForm);
$("#modal-company").on("focus", "#id_assetStartKilometer", loadkilometer);
// $("#modal-company").on("focus", "#id_assetStartTime", loadTime);
$("#modal-company").on("focus", "#id_assetTotlaKilometer", subkilometer);
$("#modal-company").on("focus", "#id_assetTotalTime", subTime);
$("#modal-company").on("click", ".create-next", applyForm);
// Delete book
$("#company-table").on("click", ".js-delete-ringAmar", loadForm);
$(".savetableinfo").on("click", senddata);
$("#modal-company").on("submit", ".js-ringAmar-delete-form", saveForm);
//$("#company-table").on("click", ".js-update-wo", initxLoad);
});
