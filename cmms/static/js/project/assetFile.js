$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-assetFiles").click(function () {
    $("#assetFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#assetFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_assetFile").html(
          data.result.html_assetFile_list
        );
      }
    }

  });

});
