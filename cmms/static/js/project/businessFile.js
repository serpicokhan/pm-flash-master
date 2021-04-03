$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-businessFiles").click(function () {
    $("#businessFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#businessFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_businessFile").html(
          data.result.html_businessFile_list
        );
      }
    }

  });

});
