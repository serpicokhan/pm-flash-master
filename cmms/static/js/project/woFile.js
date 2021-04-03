$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-woFiles").click(function () {
    $("#woFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#woFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      console.log(data);
      if (data.result.is_valid) {
        $("#tbody_woFile").html(
          data.result.html_woFile_list
        );
      }
    },
    error:function(){
      alert("123");
    },
    send:function (e, data) {
    console.log(e);
  },
  always:function (e, data) {
  console.log(e);
},

  });

});
