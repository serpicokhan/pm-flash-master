$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-taskGroupFiles").click(function () {
    $("#taskGroupFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#taskGroupFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_taskGroupFile").html(
          data.result.html_taskGroupFile_list
        );
      }
    }

  });

});
