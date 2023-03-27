$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-projectFiles").click(function () {
    $("#projectFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#projectFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_projectFile").html(
          data.result.html_projectFile_list
        );
      }
    }

  });

});
