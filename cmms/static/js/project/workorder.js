
$(function () {
  var chkselection=function(){
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    if(matches.length>0)
    {
    $(".js-create-wo-copy").show();
  }
  else{
    $(".js-create-wo-copy").hide();

  }

  };
  var clone_asset_wo2 =function () {



    matches=[];
    $(".selection-box2:checked").each(function() {
        matches.push(this.value);
    });

    // var form = $(this);

     $.ajax({
      url: '/WorkOrder/save_copy/?q='+matches+'&id='+$("#cpswoid").val(),

      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        if(data.form_is_valid)
        {
          $("#modal-copy").modal("hide");
        $("#tbody_company").html(data.html_swo_list);
        $(".assetPaging").html(data.html_swo_paginator);
        // $("tr").on("click", showAssetDetails);
        toastr.success("کپی با موفقیت انجام شد")
      }
      else
      {
        toastr.error("خطا در کپی دارایی");
      }
    }
    });
 return false;


  };

  var searchAsset=function(){


    $.ajax({
      url: '/SWorkOrder/copy/AssetSearch?q='+$("#assetSearch").val()+"&asset_loc="+$("#asset_loc").val()+"&asset_cat="+$("#asset_cat").val(),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        // $("#modal-copy").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");

        $("#tbody_company2").html(data.modalcopyasset);
        $(".assetPaging").html(data.html_asset_paginator);

          // $(".assetSearch").on("input",searchAsset);



      },error:function(){
      }
    });

  }
  var LoadFormCopySelector =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
        matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);


    return $.ajax({
      url: $(this).attr("data-url")+'?id='+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-copy").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        //alert("3123@!");
        console.log("!");
        $("#modal-copy .modal-content").html(data.modalcopyasset);
          $(".assetPaging").html(data.html_asset_paginator);
          $(".assetSearch").on("input",searchAsset);




      }
    });



};
var saveCopy= function () {
   var form = $(this);

   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     beforeSend:function(xhr, opts){

     },
     success: function (data) {
       console.log(data)
       if (data.form_is_valid) {
         //alert("Company created!");  // <-- This is just a placeholder for now for testing
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_wo_list);
         $(".woPaging").html(data.html_swo_paginator);
         $("#modal-copy").modal("hide");


         $("#issavechanged").val("1");

        // console.log(data.html_wo_list);
       }
       else {

         $("#company-table tbody").html(data.html_wo_list);
         // $("#modal-company .modal-content").html(data.html_wo_form);
         toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");
       }
     }
   });
   return false;
 };




  var loadForm =function (btn1) {

    var btn=0;
    //console.log(btn1);
    if($(btn1).attr("type")=="click")
    btn=$(this);
    else {
      btn=btn1;
    }
    //console.log($(btn).attr("type"));
    //console.log($(btn).attr("data-url"));
    return $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");
        $("#modal-company .modal-content").html('');
        $("#modal-company").modal({backdrop: 'static', keyboard: false});


      },
      success: function (data) {

        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_wo_form);
        $('#id_requiredCompletionDate').pDatepicker({
          format: 'YYYY-MM-DD',
          autoClose: true,
          initialValueType: 'gregorian'
        });
        if($('#id_datecreated').val().length>0)
        {
          $('#id_datecreated').pDatepicker({
            format: 'YYYY-MM-DD',
            initialValueType: 'gregorian',
            autoClose:true


          });
        }//id_dateCompleted
        else {

          $('#id_datecreated').pDatepicker({
            format: 'YYYY-MM-DD',
            initialValueType: 'gregorian',
            autoClose:true


          }).val('');
        }
        if($('#id_timecreated').val().length==0)
        {
          $('#id_timecreated').val(new Date().toLocaleTimeString('en-US', { hour12: false }))

        }//id_dateCompleted

        //console.log($('#id_dateCompleted').val()+":dsadsa");
        if($('#id_dateCompleted').val().length>0){
          $('#id_dateCompleted').pDatepicker({
            format: 'YYYY-MM-DD',

            autoClose:true,
            initialValueType: 'gregorian'
          });//id_dateCompleted
        }
        else {
          $('#id_dateCompleted').pDatepicker({
            format: 'YYYY-MM-DD',

            autoClose:true,
            initialValueType: 'gregorian'
          }).val('');//id_dateCompleted
        }

        //id_completedByUser

        $("#id_woAsset").change(function(){
          if($(this).val()!="-1")
          {
            $.ajax({
              url: $("#lastWorkOrderid").val()+'/'+$("#id_woAsset").val()+'/setAsset/',
              type:'get',
              dataType: 'json',
              success: function (data) {
                // console.log("hahaha");

              }
            });
          }
          else {
            // $('#id_woAsset').val("1982");
            // $('.selectpicker').selectpicker('refresh')
            $("#modal-woAsset").modal({backdrop: 'static', keyboard: false});
            $.ajax({
              url: '/Asset/WoAsset/Create',
              type:'get',
              dataType: 'json',
              success: function (data) {
                // console.log("hahaha");
                $("#modal-woAsset .modal-content").html(data.html_asset_form);

              }
            });

          }


        });
        $("#id_woAsset option:first").after('<Option value="-1">"<b>اضافه کردن عنوان جدید</b>"</option>');
        $('.selectpicker').selectpicker();
        $('.basicAutoComplete').autoComplete();
        initLoad();
        initWoPartLoad();
        initWoMeterLoad();
        initWoMiscLoad();
        initWoNotifyLoad();
        initWoFileLoad();initWoLogLoad();
        initWoPertLoad();
        $('#woassetrefresh').click(function(){

          $(this).html('<i class="fa fa-refresh fa-spin"></i>');
          $.ajax({
            url: '/WorkOrder/LoadAsset/',

            type: 'get',
            dataType: 'json',
            success: function (data) {
              if (data.form_is_valid) {
                //alert("Company created!");  // <-- This is just a placeholder for now for testing
                $("#id_woAsset").html(data.html_assets_dynamics);
                $('#woassetrefresh').html('<i class="fa fa-refresh"></i>');
                $('#id_woAsset').selectpicker('refresh');

                // $("tr").on("click", showAssetDetails);

                // console.log(data.html_asset_list);
              }
              else {

                toastr.error("خطایی بوجود آمده لطفا مجددا سعی نمایید");
              }
            }
          });

        });
        $('.advanced2AutoComplete4').autoComplete({
          resolver: 'custom',
          noResultsText:'بدون نتیجه',
          formatResult: function (item) {
            return {
              value: item.id,
              text: "[" + item.assetCode + "] " + item.assetName,
            };
          },
          events: {
            search: function (qry, callback) {
              // let's do a custom ajax call
              $.ajax(
                '/Asset/GetAssets',
                {
                  data: { 'qry': qry}
                }
              ).done(function (res) {
                callback(res);
              });
            },
          }
        });
        $('.advanced2AutoComplete4').on('autocomplete.select', function (evt, item) {
          // alert("!23");
          $("#id_woAsset").val(item.id);
          $.ajax({
            url: $("#lastWorkOrderid").val()+'/'+$("#id_woAsset").val()+'/setAsset/',
            type:'get',
            dataType: 'json',
            success: function (data) {
              // console.log("hahaha");
              console.log(data);
              if(data.asset_user){
                console.log(data.asset_user);
              $('#id_assignedToUser').val(data.asset_user);

  // Refresh the Bootstrap selectpicker to update the selected option
            $('.selectpicker').selectpicker('refresh');
          }

            }
          });
        });




      }

    });
    // $("#id_assignedToUser").chosen('.chosen-select-width': {
    //           width: "95%"
    //     });



  };

  var LoadFormSetEm =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
      matches.push(this.value);
    });

    swal({
      title: "تبدیل به EM",
      text:"",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "بلی",
      cancelButtonText: "خیر",
      closeOnConfirm: true
    }, function () {
      $.ajax({
        url: '/WorkOrder/bulkEm/'+matches,
        data: matches,
        type: 'get',
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            //alert("Company created!");  // <-- This is just a placeholder for now for testing
            $("#tbody_company").empty();
            $("#tbody_company").html(data.html_wo_list);
            // alert("!23");
            $("#modal-woEM").modal("hide");
            // $("tr").on("click", showAssetDetails);

            // console.log(data.html_asset_list);
          }
          else {

            $("#company-table tbody").html(data.html_asset_list);
            $("#modal-assetcategory .modal-content").html(data.html_asset_form);
          }
        }
      });

    });




  };
  var LoadFormsetDelete =function () {
    var matches = [];
    $(".selection-box:checked").each(function() {
      matches.push(this.value);
    });
    // console.log(matches);


    return $.ajax({
      url: $(this).attr("data-url")+matches,
      type: 'get',
      // data: {'action[]': matches},



      beforeSend: function () {



        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {

        //alert("3123@!");

        $("#modal-company .modal-content").html(data.html_wo_form);





      }

    });




  };

  var cancelform=function(){

    return $.ajax({
      url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/cancel/',
      type: 'post',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        // alert("321321");


      },
      success: function (data) {
        // console.log(data);
        if(data.form_is_valid)
        {
          swal("حذف شد!", $("#id_summaryofIssue").val(), "success");
          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);



        }
        else {

        }

      }

    });

  }

  //$("#modal-company").on("submit", ".js-company-create-form",
  var saveForm= function () {
    var urlParams = new URLSearchParams(window.location.search);
    var page = urlParams.get("page");
    var pgnum=$("#pgnum").val()||page;
    var form = $(this);
    const _url=form.attr('action')+'?q='+$('#woSearch').val()+'&page='+pgnum;


    $.ajax({
      url: _url,
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend:function(xhr,opt)
      {
        if(!$(this)[0].url.includes('delete')){
          if($("#id_woAsset").val().length<1)
          {
            toastr.error("برای دستور کار، تجهیزی انتخاب نشده است");
            xhr.abort();
          }
          if($("#id_summaryofIssue").val().length<1)
          {
            toastr.error("اطلاعات مربوط به خلاصه مشکل را وارد نمایید!");
            xhr.abort();
          }

          // if($("#havetasks").val()=="-1")
          // {
          //   toastr.error("فعالیتی مشخص نکرده اید!");
          //   xhr.abort();
          // }
          if($("#id_timecreated").val()=="")
          {
            toastr.error("زمان ایجاد فعالیت را مشخص نکردیه اید");
            xhr.abort();
          }



        }


      },
      success: function (data) {
        if (data.form_is_valid) {

          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
          $("#modal-company").modal("hide");
          toastr.success("دستور کار با موفقیت  ایجاد شد");
          $("#issavechanged").val("1");


          // console.log(data.html_wo_list);
        }
        else {



          if(data.form_err_code==1)
          {
            toastr.error(data.form_err_msg);
          }
          else {
            $("#company-table tbody").html(data.html_wo_list);
            $("#modal-company .modal-content").html(data.html_wo_form);
            toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");


          }

        }
      }
    });
    return false;
  };
  var applyForm= function () {

    var form = $(this).parent().parent();
    if(!form.attr("action"))
    {
      form=$("#js-wo-create-form");
    }


    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend:function(xhr,opt)
      {
        if(!$(this)[0].url.includes('delete')){
          if($("#id_woAsset").val().length<1)
          {
            toastr.error("برای دستور کار، تجهیزی انتخاب نشده است");
            xhr.abort();
          }
          if($("#id_summaryofIssue").val().length<1)
          {
            toastr.error("اطلاعات مربوط به خلاصه مشکل را وارد نمایید!");
            xhr.abort();
          }
          if($("#id_assignedToUser").val().length<1)
          {
            toastr.error("کاربر را مشخص کنید");
            xhr.abort();
          }


          if($("#id_timecreated").val()=="")
          {
            toastr.error("زمان ایجاد فعالیت را مشخص نکردیه اید");
            xhr.abort();
          }



        }


      },
      success: function (data) {
        if (data.form_is_valid) {


          //alert("Company created!");  // <-- This is just a placeholder for now for testing

          toastr.success("دستور کار با موفقیت  ایجاد شد");
          $("#issavechanged").val("1");
          $("#lastWorkOrderid").val(data.id);
          $("#tbody_task").html(data.first_task_created);


          // console.log(data.html_wo_list);
        }
        else {



          if(data.form_err_code==1)
          {
            toastr.error(data.form_err_msg);
          }
          else {
            $("#company-table tbody").html(data.html_wo_list);
            $("#modal-company .modal-content").html(data.html_wo_form);
            toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");


          }

        }
      }
    });
    return false;
  };
  var saveFormsetForm= function () {

    var form = $(this);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend:function(xhr,opt)
      {



      },
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("table").find("tr:gt(2)").remove();
          $(data.html_formset_list).insertAfter('table > tbody > tr:nth-child(1)');
          // $("table > tbody").html(data.html_formset_list);
          $("#modal-company").modal("hide");
          toastr.success("دستورکارها با موفقیت حذف شدند");


          // console.log(data.html_wo_list);
        }
        else {



          if(data.form_err_code==1)
          {
            toastr.error(data.form_err_msg);
          }
          else {
            $("#company-table tbody").html(data.html_wo_list);
            $("#modal-company .modal-content").html(data.html_wo_form);
            toastr.error("خطا در ایجاد دستور کار. لطفا ورودیهای خود را کنترل نمایید.");


          }

        }
      }
    });
    return false;
  };
  //############# Time Change ############################
  var getListWorkorderLastTime= function (n) {

    myurl="";
    if(n===2)
    myurl='/WorkOrder/ListCurrentWeek';
    else if(n===3) {
      myurl='/WorkOrder/ListCurrentMonth';
    }
    else {
      myurl='/WorkOrder/ListCurrentDay';
    }

    $.ajax({
      url: myurl,

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

          $("#modal-company").modal("hide");
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
  };
  ////////////////Search buttom click#############################
  var searchWorkorderByTags= function (searchStr) {

    var woStatus=$("#status-selector2").val();
    $.ajax({
      url: `/WorkOrder/Search/?q=${searchStr}&status=${woStatus}`,

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();


          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

          // $("#modal-company").modal("hide");
          // console.log(data.html_amar_list);
        }
        else {


        }
      },
      error: function (jqXHR, exception) {
        // alert(exception);
        console.error(exception);
      }
    });
    return false;
  };
  ///
  var filter= function () {

    var status_selector=($("#status-selector").val()!=null)?'?q='+$("#status-selector").val():'';
    console.log(status_selector);


    $.ajax({
      url: '/WorkOrder/'+$("#wodt1").val()+'/'+$("#wodt2").val()+'/0/'+$("#ordercol").val()+'/filter/'+$('#ordertype').val()+status_selector,

      type: 'GET',
      dataType: 'json',
      success: function (data) {

        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();

          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

          // $("#modal-company").modal("hide");
          // console.log(data.html_amar_list);
        }
        else {


        }
      },
      error: function (jqXHR, exception) {
        // alert(exception);
        console.error(jqXHR)
      }
    });
    return false;
  };
  /////////////////////////////
  function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }
  $('#woSearch').keyup(function(e){
    // setTimeout(() => {  console.log("World!"); }, 2000);
    // sleep(2000);
    // console.log(e);
    // e.cancle();
    strTag=$("#woSearch").val();
    if(strTag.length==0)
    strTag='empty_'
    strTag=strTag.replace(' ','_');

    searchWorkorderByTags(strTag);
    //alert("salam");

  });
  ////////////////////////////////////////////////////////////////
  //############# Time Radio Button هفته###################
  $('#option2').change(function(){

    getListWorkorderLastTime(2);
  });
  //################### ماه #####################
  $('#option3').change(function(){

    getListWorkorderLastTime(3);
  });

  $('#option1').change(function(){

    getListWorkorderLastTime(1);
  });

  var initLoad=function()
  {
    //alert("initload");
    $.ajax({

      url: '/Task/'+$("#lastWorkOrderid").val()+'/listTask',



      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_task").empty();
          $("#tbody_task").html(data.html_task_list);
          if(data.is_not_empty){
            $("#havetasks").val("1");
          }
          $("#modal-task").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#task-table tbody").html(data.html_task_list);
          $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });


    return false;
  };


  var initWoPartLoad=function(){

    $.ajax({

      url: '/WoPart/'+$("#lastWorkOrderid").val()+'/listWoPart',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {
          //alert("response");
          //alert(data.html_woPart_list);  // <-- This is just a placeholder for now for testing
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
    return false;
  };
  var initWoMeterLoad=function(){

    $.ajax({

      url: '/WoMeter/'+$("#lastWorkOrderid").val()+'/listWoMeter',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {
          //alert("response");
          //alert(data.html_woMeter_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_woMeter").empty();
          $("#tbody_woMeter").html(data.html_woMeter_list);
          $("#modal-woMeter").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woMeter-table tbody").html(data.html_woMeter_list);
          $("#modal-woMeter .modal-content").html(data.html_woMeter_form);
        }
      }
    });
    return false;
  };


  var initWoMiscLoad=function(){

    $.ajax({

      url: '/WoMisc/'+$("#lastWorkOrderid").val()+'/listWoMisc',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {
          //alert("response");
          //alert(data.html_woMisc_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_woMisc").empty();
          $("#tbody_woMisc").html(data.html_woMisc_list);
          $("#modal-woMisc").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woMisc-table tbody").html(data.html_woMisc_list);
          $("#modal-woMisc .modal-content").html(data.html_woMisc_form);
        }
      }
    });
    return false;
  };

  var initWoNotifyLoad=function(){

    $.ajax({

      url: '/WoNotify/'+$("#lastWorkOrderid").val()+'/listWoNotify',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {
          //alert("response");
          //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_woNotify").empty();
          $("#tbody_woNotify").html(data.html_woNotify_list);
          $("#modal-woNotify").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woNotify-table tbody").html(data.html_woNotify_list);
          $("#modal-woNotify .modal-content").html(data.html_woNotify_form);
        }
      }
    });
    return false;
  };
  var initWoPertLoad=function(){

    $.ajax({

      url: '/WoPert/'+$("#lastWorkOrderid").val()+'/listWoPert',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {
          //alert("response");
          //alert(data.html_woNotify_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_woPert").empty();
          $("#tbody_woPert").html(data.html_woPert_list);
          $("#modal-woPert").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woPert-table tbody").html(data.html_woPert_list);
          $("#modal-woPert .modal-content").html(data.html_woPert_form);
        }
      }
    });
    return false;
  };


  var initWoFileLoad=function(){

    $.ajax({

      url: '/WoFile/'+$("#lastWorkOrderid").val()+'/listWoFile',



      success: function (data) {
        //alert($("#lastWorkOrderid").val());
        if (data.form_is_valid) {


          //alert(data.html_woFile_list);  // <-- This is just a placeholder for now for testing
          $("#tbody_woFile").empty();
          $("#tbody_woFile").html(data.html_woFile_list);
          $("#modal-woFile").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {

          $("#woFile-table tbody").html(data.html_woFile_list);
          $("#modal-woFile .modal-content").html(data.html_woFile_form);
        }
      }
    });
    return false;
  };
  var initWoLogLoad=function(){


    $.ajax({

      url: '/WoLog/'+$("#lastWorkOrderid").val()+'/listWoLog/',



      success: function (data) {
        // console.log(data);

        if (data.form_is_valid) {
          // alert("!23");


          $("#tbody_wolog").empty();
          $("#tbody_wolog").html(data.html_wolog_list);
          $("#modal-wolog").modal("hide");
          //console.log(data.html_wo_list);
        }
        else {
          // alert("fdfds");

          $("#wolog-table tbody").html(data.html_woFile_list);
          // $("#modal-wolog .modal-content").html(data.html_woFile_form);
        }
      }
    });
    return false;
  };


  var loadPdate=function()
  {
    $('#id_requiredCompletionDate').pDatepicker({
      format: 'YYYY-MM-DD',
      autoClose: true,
      initialValueType: 'gregorian'
    });
    $('#id_datecreated').pDatepicker({
      format: 'YYYY-MM-DD',
      timePicker: {
        enabled: true
      },

      autoClose: true,
      initialValueType: 'gregorian'
    });//id_dateCompleted
    $('#id_dateCompleted').pDatepicker({
      format: 'YYYY-MM-DD',
      timePicker: {
        enabled: true
      },
      autoClose:true,
      initialValueType: 'gregorian'
    });//id_dateCompleted

  }

  var myWoLoader= function(){
    btn=$(this);
    //console.log(btn);
    // $.when(loadForm(btn)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad,initWoPertLoad);

    loadForm(btn);

    //initLoad();
  }
  var filterWo=function(id){
    return $.ajax({
      url: '/WorkOrder/'+id+'/getType/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");


      },
      success: function (data) {
        console.log(data);
        if(data.form_is_valid)
        {
          // alert("!23");

          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator)

        }

      }

    });
  }

  $("#woType").change(function(){
    filterWo($("#woType").val());
  });
  //////////////////////////////////////////////
  var filterWoGroup=function(id){
    return $.ajax({
      url: '/WorkOrder/'+id+'/getGroup/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");


      },
      success: function (data) {

        if(data.form_is_valid)
        {
          // alert("!23");

          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
          $(".woPaging").html(data.html_wo_paginator);

        }

      }

    });
  }






  $("#woGroup").change(function(){
    filterWoGroup($("#woGroup").val());
  });
  var saveWoEmForm= function () {
    var form = $(this);
    $.ajax({

      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_wo_list);
          // alert("!23");
          $("#modal-woEM").modal("hide");
          // $("tr").on("click", showAssetDetails);

          // console.log(data.html_asset_list);
        }
        else {

          $("#company-table tbody").html(data.html_asset_list);
          $("#modal-assetcategory .modal-content").html(data.html_asset_form);
        }
      }
    });
    return false;
  };
  /////////////
  var updatetaskuser=function(){
    // alert(1000);
    // alert($("#id_assignedToUser").val());
    user_id=$("#id_assignedToUser").val();
    // alert(user_id.length);
    // console.log(user_id,user_id.length);


    return $.ajax({
      url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/Task/'+user_id+'/Update_Task_User/',

      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        if(data.form_is_valid)
        {
          // $("#modal-copy").modal("hide");
          $("#tbody_task").html(data.html_data_tasks);
          // $(".assetPaging").html(data.html_swo_paginator);
          // $("tr").on("click", showAssetDetails);
          toastr.success("کاربر با موفقیت بروز شد");
        }
        else
        {
          toastr.error("خطا در بروز رسانی کاربر در کپی دارایی");
        }
      }
    });
    return false;

  }
  /////////////
  var ExportWO=function(){
    // alert(1000);
    // alert($("#id_assignedToUser").val());
    // user_id=$("#id_assignedToUser").val();
    // alert(user_id.length);
    // console.log(user_id,user_id.length);

    var form=$(this).attr('data-url');
    window.open(form, '_blank');
    return false;

  }
  var filter_by_woStatus=function(){
    var search_str=$("#woSearch").val()||'#'
    window.location.replace("/WorkOrder/list_wo_by_status/"+$("#status-selector2").val()+`?q=${search_str}`);
  }


  var wobulkdeletion_pressed=function(){
    swal({
      title:"حذف دستور کار",
      text: "",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "بلی",
      cancelButtonText: "خیر",
      closeOnConfirm: true
    }, function () {
      wobulkdeletion();

    });
  }
  var wobulkdeletion =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
      matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);

    var urlParams = new URLSearchParams(window.location.search);
    var page = urlParams.get("page");
    return $.ajax({
      url: '/WorkOrder/BulkDelete/'+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {



      },
      success: function (data) {
        if(data.form_is_valid)
        {
          window.location.replace("/WorkOrder/?page="+page);
        }
        else
        {
          toastr.error("خطا در حذف دسته ای دستورکار");
        }
      }
    });
  };

  //
  var wobulkcompletion_pressed=function(){
    swal({
      title:"تکمیل دستور کار",
      text: "",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "بلی",
      cancelButtonText: "خیر",
      closeOnConfirm: true
    }, function () {
      wobulkcompletion();

    });
  }
  var wobulkcompletion =function () {
    matches=[];
    $(".selection-box:checked").each(function() {
      matches.push(this.value);
    });
    // lo(matches);
    // console.log(matches);

    var urlParams = new URLSearchParams(window.location.search);
    var page = urlParams.get("page");
    return $.ajax({
      url: '/WorkOrder/BulkComplete/'+matches,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {



      },
      success: function (data) {
        if(data.form_is_valid)
        {
          window.location.replace("/WorkOrder/?page="+page);
        }
        else
        {
          toastr.error("خطا در تکمیل دستور کار");
        }
      }
    });
  };
  //
  var check_wo_is_new=function(){
    if($("#lastWorkOrderid").val()!="0")
    {
    }
    else{
      applyForm();

    }
  }
var check_completion_date=function()
{
  old_status=$("#id_woStatus").val();
  if(old_status=="7")
  {
    return $.ajax({
      url: '/WorkOrder/'+$("#lastWorkOrderid").val()+'/ChangeStatus/'+old_status,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {



      },
      success: function (data) {
        if(data.form_is_valid)
        {
          // console.log(data);
          $("#id_dateCompleted").val(data.date_compeletd);
          $("#id_timeCompleted").val(data.time_compeletd);
          // alert("123");
        }
        else
        {
          // console.log(old_status);
          $("#id_woStatus").val((data.wo_status));
          toastr.error("فعالیت باز! دستور کار نمی توناند در این وضعیت قرار بگیرد.")
        }
      }
    });
  }

}
  $(".js-create-wo").unbind();
  $("#modal-company").on("click",".js-create-task",check_wo_is_new);
  $("#modal-company").on("change","#id_woStatus",check_completion_date);

  $(".js-create-wo").click(loadForm);
  $(".js-bulk-formset-delete-wo").click(LoadFormsetDelete);
  $(".js-bulkem-selector").click(LoadFormSetEm);
  $("#modal-company").on("submit", ".js-wo-create-form", saveForm);
  $("#modal-company").on("click", ".woapply", applyForm);
  // $("#modal-company").on("click", ".btn-default", cancelform);
  // $('#modal-company').on('hidden.bs.modal',cancelform);
  // Update book
  $("#company-table").on("click", ".js-update-wo", myWoLoader);
  $("#modal-company").on("submit", ".js-wo-update-form", saveForm);
  // Delete book
  $("#company-table").on("click", ".js-delete-wo2", loadForm);

  $("#modal-company").on("submit", ".js-wo2-delete-form", saveForm);
  $("#modal-company").on("submit", ".js-formset-delete-form", saveFormsetForm);
  $("#modal-woEm").on("submit", ".js-bulkem-selector-form2", saveWoEmForm);
  $("#modal-company").on("change",'.user-assignment',updatetaskuser);

  $(".wo-filter").on("click",filter);
  $(".js-bulkwo-selector").on("click", wobulkdeletion_pressed);
  $(".js-completewo-selector").on("click", wobulkcompletion_pressed);

  $("#status-selector2").on("change",filter_by_woStatus);
  $("#company-table").on("click", ".selection-box", chkselection);
  $(".js-create-wo-copy").click(LoadFormCopySelector);
  $("#modal-copy").on("click", ".btn-save-copy", clone_asset_wo2);
  $(".woexport").on("click",  ExportWO);

  $(document).ready(function(){


    var cururl=window.location.pathname;
    if(cururl.indexOf('details')>-1)
    {

      url_parts=cururl.split('/');
      var test = $('<button/>',
      {
        text: 'Test',
        'data-url':'/WorkOrder/'+url_parts[2]+'/update/',
        click: function () {  },

      });
      // var btn={'data-url':'/WorkOrder/10/update/'};
      $.when(loadForm(test)).done(initLoad,initWoPartLoad,initWoMeterLoad,initWoMiscLoad,initWoNotifyLoad,initWoFileLoad,initWoLogLoad,initWoPertLoad);
    }
  });

  //$("#company-table").on("click", ".js-update-wo", initxLoad);
});
// js-completewo-selector
