$(function () {

  var loadForm =function (btn1) {


    var btn=0;
    //console.log(btn1);
    if($(btn1).attr("type")=="click")
     btn=$(this);
    else {
      btn=btn1;
    }
    // console.log('/TaskGroup/'+($("#id_woAsset").val().length>0)?$("#id_woAsset").val():-1+'/js/');
    //console.log($(btn).attr("type"));
    //console.log($(btn).attr("data-url"));
    return $.ajax({
      url: '/TaskGroup/'+(($("#id_woAsset").val().length)?$("#id_woAsset").val():-1)+'/js/',
      type: 'get',
      dataType: 'json',
      beforeSend: function (xhr,opts) {
        //alert(btn.attr("data-url"));
        //alert("321321");
        // /$("#modal-taskGroup").modal("hide");
        if($("#id_woAsset").val()!='')
        {
          $("#modal-taskGroup").modal({backdrop: 'static', keyboard: false});
        }
        else
        {
          toastr.error("مشخص کردن دارایی الزامی است");
          xhr.abort();
        }

      },
      success: function (data) {
        //alert("3123@!");
         $("#modal-taskGroup .modal-content").html(data.html_taskGroup_list);



      },
      error:function(){
        console.log("error");
      }
    });



};

  var loadTaskForm =function () {
    var btn=$(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function (xhr,opts) {
        //alert(btn.attr("data-url"));
        if($("#id_woAsset").val()!='')
        {
          $("#modal-task").modal({backdrop: 'static', keyboard: false});
        }
        else
        {
          toastr.error("مشخص کردن دارایی الزامی است");
          xhr.abort();
        }


      },

      success: function (data) {
        $("#modal-task .modal-content").html(data.html_task_form);
        $(".selectpicker").selectpicker();
      }
    });




};

//$("#modal-company").on("submit", ".js-company-create-form",
var saveTaskForm= function () {

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
         $("#tbody_task").empty();
         $("#tbody_task").html(data.html_task_list);
         $('#modal-task').modal('hide');
         // alert("123");
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

 var deleteTaskForm= function (event) {

   if(event.target.className=="btn btn-danger")
   {

    var form = $(this);


    $.ajax({
      async: true,
      url: form.attr("data-url"),
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing
          $("#tbody_task").empty();
          $("#tbody_task").html(data.html_task_list);
          $('#modal-task').modal('hide');

          //console.log(data.html_wo_list);
        }
        else {

          $("#task-table tbody").html(data.html_task_list);
          $("#modal-task .modal-content").html(data.html_task_form);
        }
      }
    });
  }
    return false;
  };
var set_task_result=function(){
  e=$(this).parent();
  if($(this).val().length>0){
  $.ajax({
    async: true,
    url: '/Task/'+$(this).attr("data-url")+'/set_task_result/?q='+$(this).val(),

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        // e=$(this).parent();
        e.html('');
        e.html('<span>'+data.result+'</span>');


      }


    }
  });
}
return false;

};
//بدست آودن مدت زمان مجموع کاری یک کاربر در یک تاریخ
var get_task_user_time=function(){

  $.ajax({
    async: true,
    url: '/Task/GetTotalEstimatedUserTime/'+$("#lastWorkOrderid").val()+'/'+$("#id_taskAssignedToUser").val(),

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        // console.log(data.result.taskTimeEstimate__sum);
        if(data.result.taskTimeEstimate__sum>=0)

          $("#assnamelabel").text(`زمان تقریبی ${data.result.taskTimeEstimate__sum} ساعت`);


      }


    }
  });

return false;

};
var set_task_completion_time_auto=function(){
  if($("#set-auto-completion-time").attr("date-url")!="None")
  {
  $.ajax({
    async: true,
    url: '/Task/get_auto_completion_time/'+$("#set-auto-completion-time").attr("date-url"),

    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#id_taskDateCompleted").val(data.date);
        $("#id_taskTimeCompleted").val(data.time);


      }


    }


  });

return false;
}
return;

};



 // Create book
$(".js-create-taskGroup").unbind();
$(".js-delete-task").unbind();
$(".js-update-task").unbind();

$(".js-create-task").unbind();

$(".js-create-task").click(loadTaskForm);
$(".js-create-taskGroup").click(loadForm);
$("#task-table").on("click", ".js-update-task", loadTaskForm);
// $("#modal-task").on("submit", ".js-task-update-form", saveTaskForm);
// Delete book
$("#task-table").on("click", ".js-delete-task", loadTaskForm);
$("#modal-task").on("click", ".js-task-delete-form", deleteTaskForm);
$("#modal-task").on("change", ".ttttt", get_task_user_time);
$("#modal-task").on("click", ".set-auto-completion-time", set_task_completion_time_auto);
$("#task-table").on("focusout", ".task-result", set_task_result );

});
