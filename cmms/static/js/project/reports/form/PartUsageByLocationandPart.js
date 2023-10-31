$(function () {

$("#id_makan").change(function(){
  mak_val=0;
  const noe=$("#id_assetType").val()||'0';
  if(!$("#id_makan").val())
    mak_val=-1;
  else
    mak_val=$("#id_makan").val();
  alert(noe);
  $.ajax({
    url: '/Asset/Info?makan='+mak_val+'&noe='+noe,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
      $("#id_assetname").html(data.html_assets_dynamics);
      $('#id_assetname').selectpicker('refresh');
      }
      else {

      toastr.error("خطایی بوجود آمده لطفا مجددا سعی نمایید");
      }
    }
  });
});
//
$("#id_assetType").change(function(){
  mak_val=0;
  if(!$("#id_makan").val())
    mak_val=-1;
  else
    mak_val=$("#id_makan").val();
  $.ajax({
    url: '/Asset/Info?makan='+mak_val+'&noe='+$("#id_assetType").val(),
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("Company created!");  // <-- This is just a placeholder for now for testing
      $("#id_assetname").html(data.html_assets_dynamics);
      $('#id_assetname').selectpicker('refresh');
      }
      else {

      toastr.error("خطایی بوجود آمده لطفا مجددا سعی نمایید");
      }
    }
  });

});
//
});
