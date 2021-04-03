$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-userFile").click(function () {
    $("#userFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#userFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_userFile").html(
          data.result.html_userFile_list
        );
      }
    }
  });

});
