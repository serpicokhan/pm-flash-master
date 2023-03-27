$(function(){
  var show_status_alert=function(){
  var status=$(this).attr('date-url');
  Swal.fire({
  title: 'Are you sure?',
  text: 'Do you want to continue?',
  type:'warning',
  confirmButtonText: "بلی",
      cancelButtonText: "خیر",
      showCancelButton: true,

}).then((result) => {
  if (result.value) {
    change_statuse(status);
    // execute code for "Yes" response
  } else {
    alert("2");
    // execute code for "No" response
  }
});

}
var change_statuse=function(status){
  // alert("1");
  // var status=$(this).attr('date-url');
  console.log(status);


  matches=[];
  $(".custom-control-input:checked").each(function() {
    matches.push(this.value);
  });
  // console.log(matches);
  $.ajax({
    url: '/Purchase/Item/Change_Status/?q='+matches+'&status='+status,

    type: 'get',
    dataType: 'json',
    beforeSend: function () {

    },
    success: function (data) {
      if(data.form_is_valid)
      {
        // $("#modal-copy").modal("hide");
        $("#orders").empty();
        $("#orders").html(data.html_purchaseRequest_list);
        // $(".assetPaging").html(data.html_swo_paginator);
        // alert("it is done!");
        // // $("tr").on("click", showAssetDetails);
        // toastr.success("کپی با موفقیت انجام شد")
      }
      else
      {
        toastr.error("خطا در کپی دارایی");
      }
    }
  });
}
$("#purchaseItem_table").on("click", ".js-update-purchaseRequestStatus", show_status_alert);
});
