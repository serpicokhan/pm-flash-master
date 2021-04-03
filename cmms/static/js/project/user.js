
$(function () {


  var loadForm =function (btn1) {
    var btn=0;
    if($(btn1).attr("type")=="click")
     btn=$(this);
    else {
      btn=btn1;
    }

    return $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {

        $("#modal-company").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {

        $("#modal-company .modal-content").html(data.html_user_form);
        var elem = document.querySelector('.js-switch');
        var init = new Switchery(elem);
        $("#id_userStatus").change(function(){
          js_switch_change();
        });
      }

    });
};
var cancelForm=function(){
// alert("!23");
  $.ajax({
    url: '/User/'+$("#lastUserId").val()+'/Cancel/',

    type: 'post',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        //alert("taskGroup created!");  // <-- This is just a placeholder for now for testing

        $("#tbody_company").empty();
        $("#tbody_company").html(data.html_user_list);

        $('tr').on('click',function(){
        $('#leftProfileImage').attr('src',($(this).find('img').attr('src')));
        $("#userName").html($(this).find("td:eq(2)").text());
        $('.userDetailInfo').show();
        userDetails($(this).attr('data-url'));
        });


        // $("#modal-taskGroup").modal("hide");
       // console.log(data.html_taskGroup_list);
      }
      else {

        // $("#company-table tbody").html(data.html_part_list);
        // $("#modal-company .modal-content").html(data.html_part_form);
      }
    }
  });
  return false;


};

var js_switch_change=function()
{
  $.ajax({
    url: '/User/'+$("#lastUserId").val()+'/eval/',
    type: 'get',
    dataType: 'json',

    success: function (data) {
    },
    error:function(x,y,z)
    {
      alert("123");
    }
  });
}

var getUserStatusUrl=function(statusCode)
{
  switch (statusCode) {
    case "0":
      return '/User/listActiveUser/';
      break;
    case "1":
    return '/User/listAllUser/';

      break;
    case "2":
    return '/User/listInActiveUser/';

      break;


  }
}
$("#userStatus").change(function(){

  $.ajax({

    url: getUserStatusUrl($("#userStatus").val()),
    type: 'get',
    dataType: 'json',
    beforeSend:function()
    {

      alert(getUserStatusUrl($("#userStatus").val()));
    },
    success: function (data) {

      $("#tbody_company").empty();
      $("#tbody_company").html(data.html_user_list);
      $(".userPaging").html(data.html_user_paginator);
      // $("#modal-company").modal("hide");

      //console.log(data.html_assetLife_form)
    },
    error:function(x,y,z)
    {
      console.log(x.responseText);
    }
  });
});

var userSearch=function(name)
{
  if(name.length==0)
    name='_'
  $.ajax({

    url: '/User/'+name+'/Search/',
    type: 'get',
    dataType: 'json',
    beforeSend:function()
    {

      console.log(name);
    },
    success: function (data) {

      $("#tbody_company").empty();
      $("#tbody_company").html(data.html_user_list);
      // $(".userPaging").html(data.html_user_paginator);
      // $("#modal-company").modal("hide");

      //console.log(data.html_assetLife_form)
    },
    error:function(x,y,z)
    {
      console.log(x.responseText);
    }
  });

}
$("#userSearch").keyup(function(){
  userSearch($("#userSearch").val());
});


var saveForm= function (e) {
     e.preventDefault();
     var form2 = $(this);

   var form = new FormData(document.getElementById("userform"));
   // console.log(form);
   $.ajax({
     url: form2.attr("action"),
     data: form,
     type: form2.attr("method"),
     dataType: 'json',
     cache:false,
     contentType: false,
     processData: false,
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_company").empty();
         $("#tbody_company").html(data.html_user_list);
         $("#modal-company").modal("hide");


       }
       else {
         $("#company-table tbody").html(data.html_user_list);
         $("#modal-company .modal-content").html(data.html_user_form);
       }
     },
     error:function(x,y,z)
     {
       alert(x.status);
       console.log(y);
       console.log(z);
     }
   });
   return false;
 };
 var saveForm2= function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#tbody_company").empty();
          $("#tbody_company").html(data.html_user_list);
          $("#modal-company").modal("hide");

        }
        else {
          $("#company-table tbody").html(data.html_user_list);
          $("#modal-company .modal-content").html(data.html_user_form);
        }
      },
      error:function(x,y,z)
      {
        alert("ddsds");
      }
    });
    return false;
  };
 var initUserGroupsLoad=function(){

   $.ajax({
     url: '/UserGroups/'+$("#lastUserId").val()+'/listUserGroups',
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_userGroup").empty();
         $("#tbody_userGroup").html(data.html_userGroup_list);
         $("#modal-userGroup").modal("hide");
       }
       else {
         $("#userGroup-table tbody").html(data.html_userGroup_list);
         $("#modal-userGroup .modal-content").html(data.html_userGroup_form);
       }
     }
   });
 return false;
 };

 var initUserFileLoad=function(){

   $.ajax({

     url: '/UserFile/'+$("#lastUserId").val()+'/ListUserFile',



     success: function (data) {
         //alert($("#lastWorkOrderid").val());
       if (data.form_is_valid) {


         //alert(data.html_userFile_list);  // <-- This is just a placeholder for now for testing
         $("#tbody_userFile").empty();
         $("#tbody_userFile").html(data.html_userFile_list);
         $("#modal-userFile").modal("hide");
         //console.log(data.html_wo_list);
       }
       else {

         $("#userFile-table tbody").html(data.html_userFile_list);
         $("#modal-userFile .modal-content").html(data.html_userFile_form);
       }
     }
   });
 return false;
 };


 var initUserCertLoad=function(){

   $.ajax({
     url: '/UserCertification/'+$("#lastUserId").val()+'/ListUserCert',
     success: function (data) {
       if (data.form_is_valid) {
         $("#tbody_userCertification").empty();
         $("#tbody_userCertification").html(data.html_userCertification_list);
         $("#modal-userCertification").modal("hide");
       }
       else {
         $("#userCertification-table tbody").html(data.html_userCertification_list);
         $("#modal-userCertification .modal-content").html(data.html_userCertification_form);
       }
     }
   });
 return false;
 };



  var initUserLogLoad=function(){

    $.ajax({
      url: '/UserLog/'+$("#lastUserId").val()+'/ListUserLog',
      success: function (data) {
        if (data.form_is_valid) {
          $("#tbody_userLog").empty();
          $("#tbody_userLog").html(data.html_userLog_list);
          console.log(data);

        }
        else {
          $("#userLog-table tbody").html(data.html_userLog_list);

        }
      }
    });
  return false;
  };

 var myWoLoader= function(){
   btn=$(this);
   $.when(loadForm(btn)).done(initUserGroupsLoad,initUserFileLoad,initUserCertLoad,initUserLogLoad);
 }



///////////////////////////////
var userDetails=function(id){
  $.ajax({
    url: '/User/'+id+'/DashDetails',
    success: function (data) {
      if (data.form_is_valid) {
        // $("#tbody_userLog").empty();


        stRes='<small class="label label-info">'+data.user_wo_num_current_year+' , '+data.user_wo_num_current_month+'</small>';//+'   ,   <small class="label label-primary">'+data.user_wo_num_current_month+'</small>';
        $("#userWorkOrderCount").html(stRes);
        stRes='<small class="label label-info">'+data.user_task_work_hour_year+' , '+data.user_task_work_hour_month+'</small>'//+'   ,   <small class="label label-primary">'+data.user_task_work_hour_month+'</small>'
        // stRes=data.user_task_work_hour_year+","+data.user_task_work_hour_month;
        $("#userWorkHour").html(stRes);
          stRes='<small class="label label-info">'+data.user_wo_num_ontime_year+' , '+data.user_wo_num_ontime_month+'</small>'//+'   ,   <small class="label label-primary">'+data.user_wo_num_ontime_year+'</small>'
        // stRes=data.user_wo_num_ontime_year+","+data.user_wo_num_ontime_year;
        $("#userOnTimeWorkOrder").html(stRes);
          stRes='<small class="label label-info">'+data.user_all_wo_num_current_year+' , '+data.user_all_wo_num_current_month+'</small>'//+'   ,   <small class="label label-primary">'+data.user_wo_num_ontime_year+'</small>'
        // stRes=data.user_wo_num_ontime_year+","+data.user_wo_num_ontime_year;
        $("#userAllWorkOrderCount").html(stRes);
        console.log(data);

      }
      else {
      alert("123321");

      }
    }
  });
return false;

};















$('tr').on('click',function(){
  $('#leftProfileImage').attr('src',($(this).find('img').attr('src')));
  $("#userName").html($(this).find("td:eq(2)").text());
  $('.userDetailInfo').show();


  userDetails($(this).attr('data-url'));

});
$(".js-create-user").click(loadForm);
$("#modal-company").on("submit", ".js-user-create-form", saveForm);

// Update book
$("#company-table").on("click", ".js-update-user", myWoLoader);
$("#modal-company").on("submit", ".js-user-update-form", saveForm);
// Delete book
$("#company-table").on("click", ".js-delete-user", loadForm);
$("#modal-company").on("submit", ".js-user-delete-form", saveForm2);
$('#modal-company').on('hidden.bs.modal',cancelForm);
//$("#company-table").on("click", ".js-update-user", initxLoad);
});
