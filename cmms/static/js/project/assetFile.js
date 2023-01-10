$(function () {
  $(".js-upload-assetFiles").unbind();

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-assetFiles").click(function () {
    $("#assetFileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#assetFileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      // console.log(data);
      if (data.result.is_valid) {
        $("#tbody_assetFile").html(
          data.result.html_assetFile_list
        );
      }
    }

  });
var delete_assetFile=function(){
  // alert("123");
    var btn=$(this);
    var yes=confirm("فایل حذف شود؟");
    if(yes)
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        success: function (data) {
          if(data.is_valid){
            $("#tbody_assetFile").empty();
            $("#tbody_assetFile").html(data.html_assetFile_list);
          }




        }
      });
  return false;
};
$("#assetFile-table").on("click",".js-delete-assetFile",delete_assetFile);
});
