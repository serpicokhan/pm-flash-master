$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-partFiles").click(function () {
    $("#partFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#partFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_partFile").html(
          data.result.html_partFile_list
        );
      }
    }

  });

});
