$(function () {

  var loadMiscCostCodeForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-miscCostCode").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        // alert("success");
        $("#modal-miscCostCode .modal-content").html(data.html_miscCostCode_form);
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveMiscCostCodeForm= function () {


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
         $("#tbody_miscCostCode").empty();
         $("#tbody_miscCostCode").html(data.html_miscCostCode_list);
         $("#modal-miscCostCode").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#miscCostCode-table tbody").html(data.html_miscCostCode_list);
         $("#modal-miscCostCode .modal-content").html(data.html_miscCostCode_form);
       }
     }
   });
   return false;
 };
 var deleteMiscCostCodeForm= function (event) {

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
          $("#tbody_miscCostCode").empty();
          $("#tbody_miscCostCode").html(data.html_miscCostCode_list);
          $("#modal-miscCostCode").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#miscCostCode-table tbody").html(data.html_miscCostCode_list);
          $("#modal-miscCostCode .modal-content").html(data.html_miscCostCode_form);
        }
      }
    });
  }
    return false;
  };
  var deleteMiscCostCode=function(id){
    $.ajax({
      async: true,
      url: '/SettingPage/MiscCostCode/'+id+'/Delete/',

      type: 'get',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_miscCostCode").empty();
          $("#tbody_miscCostCode").html(data.html_miscCostCode_list);
          $("#modal-miscCostCode").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {


        }
      }
    });

    return false;
  }
  $('#miscCostCode-table').on('click','.js-delete-miscCostCode', function () {
  const dashassetid=($(this).attr('data-url'));


    swal({
      title: "حذف",
      text: "حذف",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "بلی",
      cancelButtonText: "خیر",
      closeOnConfirm: true
     }, function () {
         // cancelform();
         deleteMiscCostCode(dashassetid);

     });

    // do something…
  });

 // Create book
$(".js-create-miscCostCode").click(loadMiscCostCodeForm);
//$("#task-submit").on("", ".js-task-create-form", saveTaskForm);
//s$("#task-submit").on("click",function(){alert("32132");});
//$("#task-table").on("load",initLoad);
// Update book
$("#miscCostCode-table").on("click", ".js-update-miscCostCode", loadMiscCostCodeForm);

$("#modal-miscCostCode").on("click", ".js-miscCostCode-update-form", saveMiscCostCodeForm);
// Delete book
// $("#miscCostCode-table").on("click", ".js-delete-miscCostCode", loadMiscCostCodeForm);
// $("#modal-miscCostCode").on("click", ".js-miscCostCode-delete-form", deleteMiscCostCodeForm);

});
