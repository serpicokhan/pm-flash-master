$(function () {
  var loadForm =function (btn1) {
    var btn=0;
    // console.log(btn1);
   btn=btn1;

    return $.ajax({
      url: btn.attr("data-url2"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_asset_form);
        $("#assetformupdatesubmit").hide();

        var elem = document.querySelector('.js-switch');
        var init = new Switchery(elem);
        $("#id_assetStatus").change(function(x){

          // if(x.cancelable)
          // js_switch_change();



        });
          $('.selectpicker').selectpicker();
            // $("tr").on("click", showAssetDetails);

      }
    });



};
  $(".col-lg-3").on('click',function(){

loadForm($(this));

  });
});
