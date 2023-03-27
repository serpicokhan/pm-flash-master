$(function(){

  // $('.dtpicker').bootstrapMaterialDatePicker({
  //       weekStart: 0,
  //       time: false,
  //       nowButton : true,
  //       initialValue: true,
  //       initialValueType: 'gregorian',
  //   });
    // $("#id_PurchaseDateTo").pDatepicker({
    //
    //         format: 'YYYY-MM-DD',
    //         initialValueType: 'gregorian',
    //         autoClose:true
    //
    // });

    $(".dt-picker").pDatepicker({ format: 'YYYY-MM-DD',
            initialValueType: 'gregorian',
            autoClose:true});
            xxxDate1=new persianDate();
            dt1=xxxDate1.pDate.year.toString()+"-"+("0" + xxxDate1.pDate.month).slice(-2)+"-01";
            $("#date_from").val(dt1);

    var save_msg=function(){
     document.getElementById('purchaseform').submit();
    }
    var init_load_purchase_items=function(){
      var purchase_id=$("#id_lastpurchase_id").val();
      $.ajax({
        url:`/Purchase/items/${purchase_id}`,

        type: 'get',
        dataType: 'json',
        error:function(x,y,z){
          // console.log(x.responseText);
          // alert("error");
        },
        beforeSend:function(xhr){

        },
        success: function (data) {
            $("#tbody_purchaseRequest").empty();
            // tbl_purchase_content+=data.rows;
            $("#tbody_purchaseRequest").append(data.rows);
            // ids.push(data.id);
        }
      });
    }
    var update=function(){
      window.location=$(this).attr('data-url');
    }
    init_load_purchase_items();
    $(".sub_purchase").on("click",  save_msg);
    // $(".js-create-purchaseRequest").click(myprLoader);
    $("#purchaseRequest-table").on("click", ".js-update-purchaseRequest", update);
});
