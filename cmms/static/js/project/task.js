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
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");
        // /$("#modal-taskGroup").modal("hide");
        $("#modal-taskGroup").modal({backdrop: 'static', keyboard: false});
      },
      success: function (data) {
        //alert("3123@!");

         $("#modal-taskGroup .modal-content").html(data.html_taskGroup_list);
        console.log(data);

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
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        $("#modal-task").modal({backdrop: 'static', keyboard: false});

      },
      success: function (data) {
        $("#modal-task .modal-content").html(data.html_task_form);
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
         alert("123");
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
   console.log(event.target.className);
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




 // Create book
$(".js-create-taskGroup").unbind();
$(".js-create-task").unbind();
$(".js-create-task").click(loadTaskForm);
$(".js-create-taskGroup").click(loadForm);
$("#task-table").on("click", ".js-update-task", loadTaskForm);
// $("#modal-task").on("submit", ".js-task-update-form", saveTaskForm);
// Delete book
$("#task-table").on("click", ".js-delete-task", loadTaskForm);
$("#modal-task").on("click", ".js-task-delete-form", deleteTaskForm);

});
