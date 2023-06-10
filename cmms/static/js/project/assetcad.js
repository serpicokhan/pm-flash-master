$(function () {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  // const img = new Image();
  // console.log("dasdsa");
  // img.src='http://127.0.0.1:8000/media/documents/2023/04/20/fact2.JPG';
  // img.onload = function() {
  // canvas.width = img.width;
  // canvas.height = img.height;

  // console.log(img);
  // ctx.drawImage(img, 0, 0);
// }

  let isDrawing = false;
  let startX, startY;
  let textBox, textBoxOffsetX, textBoxOffsetY;
  let flagBtn = document.getElementById('flag-btn');

  function startDragging(e) {
    textBoxOffsetX = e.clientX - textBox.offsetLeft;
    textBoxOffsetY = e.clientY - textBox.offsetTop;
    textBox.style.cursor = "move";
    canvas.addEventListener('mousemove', dragTextBox);
  }

  function stopDragging(e) {
    textBox.style.cursor = "default";
    canvas.removeEventListener('mousemove', dragTextBox);
  }

  function dragTextBox(e) {
    textBox.style.left = (e.clientX - textBoxOffsetX) + "px";
    textBox.style.top = (e.clientY - textBoxOffsetY) + "px";
  }
  $("#assetIdName").change(function(){
    return $.ajax({
      url: '/Asset/Cad/changeloc?q='+$(this).val()+'&ratiow='+window.innerWidth+'&ratioh='+window.innerHeight,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        //alert(btn.attr("data-url"));
        //alert("321321");
        // /$("#modal-maintenanceType").modal("hide");
        // $("#modal-company").modal("show");
      },
      success: function (data) {
        // console.log(data);
        // console.log("call from here");
        var canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d');
        const img = new Image();
        img.src=data.img;
        $("#location_id").val(data.id);
        img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;

        context.drawImage(img, 0, 0);
        console.log(data);
        $("#locpoints").html(data.points);
        $("[data-toggle=popover]")
        .popover({html:true})

      }
      }
    });

    // };
    //
    // img.src = 'http://127.0.0.1:8000/media/documents/fact2.JPG'; // replace with the URL of your image
  });

  // canvas.addEventListener('mousedown', e => {
  //   startX = e.offsetX;
  //   startY = e.offsetY;
  //   isDrawing = true;
  // });
  //
  // canvas.addEventListener('mousemove', e => {
  //   // img=new Image
  //   if (!isDrawing) return;
  //   const currentX = e.offsetX;
  //   const currentY = e.offsetY;
  //   const width = currentX - startX;
  //   const height = currentY - startY;
  //   ctx.clearRect(0, 0, canvas.width, canvas.height);
  //   ctx.drawImage(img, 0, 0);
  //   ctx.strokeRect(startX, startY, width, height);
  // });

  // canvas.addEventListener('mouseup', e => {
  //   isDrawing = false;
  //   const x = Math.min(startX, e.offsetX);
  //   const y = Math.min(startY, e.offsetY);
  //   const width = Math.abs(e.offsetX - startX);
  //   const height = Math.abs(e.offsetY - startY);
  //   if (width > 0 && height > 0) {
  //     textBox = document.createElement("input");
  //     textBox.type="text"
  //     textBox.style.position = "absolute";
  //     textBox.style.left = x + "px";
  //     textBox.style.top = y + "px";
  //     textBox.style.width = width + "px";
  //     textBox.style.height = height + "px";
  //     textBox.classList.add('advanced2AutoComplete');
  //     textBox.addEventListener("change", e => {
  //       console.log(e.target.value);
  //     });
  //     textBox.addEventListener('mousedown', startDragging);
  //     textBox.addEventListener('mouseup', stopDragging);
  //     pcol=document.getElementById('pcol');
  //     pcol.appendChild(textBox);
  //
  //   }
  // });

  canvas.addEventListener('click', e => {
    // console.log("here");
    const x = e.offsetX;
    const y = e.offsetY;
    // if (textBox && x >= textBox.offsetLeft && x <= textBox.offsetLeft + textBox.offsetWidth &&
    //     y >= textBox.offsetTop && y <= textBox.offsetTop + textBox.offsetHeight) {
    //   // alert(textBox.value);
    // }
    var rect = canvas.getBoundingClientRect();
    var x1 = event.clientX - rect.left;
    var y1 = event.clientY - rect.top;
    var coordinatesWidth=window.innerWidth;
    // const adjustmentRatioX = window.innerWidth / coordinates.deviceWidth;
    // const adjustmentRatioY = window.innerHeight / coordinates.deviceHeight;
    //
    // // Calculate the adjusted coordinates
    // const adjustedX = coordinates.x * adjustmentRatioX;
    // const adjustedY = coordinates.y * adjustmentRatioY;
    loadForm(x1,y1,coordinatesWidth);


  // Update the modal content with the click position
  // var clickPosition = document.getElementById("clickPosition");
  // clickPosition.innerHTML = "X: " + x1 + ", Y: " + y1;

  });

  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  var loadForm =function (x1,y1,z1) {

    //console.log($(btn).attr("type"));
    //console.log($(btn).attr("data-url"));
    if($("#location_id").val())
      return $.ajax({
        url: '/Asset/Cad/create?q='+$("#location_id").val(),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          //alert(btn.attr("data-url"));
          //alert("321321");
          // /$("#modal-maintenanceType").modal("hide");
          $("#modal-company").modal("show");
        },
        success: function (data) {
          //alert("3123@!");

          $("#modal-company .modal-content").html(data.html_asset_cad_form);
          $("#id_x").val(x1);
          $("#id_y").val(y1);
          $("#id_z").val(z1);

            $(".selectpicker").selectpicker();



        }
      });



  };
  var saveForm=function(x1,y1){

    var form = $(this);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //alert("Company created!");  // <-- This is just a placeholder for now for testing

          $("#modal-company").modal("hide");
          pcol=document.getElementById("pcol")
          // flagBtn.style.display = "block";
          // flagBtn.style.position = "absolute";
          // flagBtn.style.left = $("id_x").val() - 20 + "px";
          // flagBtn.style.top = $("id_y").val() - 20 + "px";
          // pcol.appendChild(flagBtn);
          var btn = document.createElement("button");
          var ibut = document.createElement("i");
          pcol.appendChild(btn);
          // document.body.appendChild(btn);
          btn.style.position = "absolute";
          btn.style.left = $("#id_x").val() + "px";
          btn.style.top = $("#id_y").val() + "px";
          // btn.innerHTML = "btn";
          btn.classList.add("btn");
          btn.classList.add("btn-danger");
          btn.classList.add("dim");
          btn.appendChild(ibut);
          btn.setAttribute('data-url',form.find("#id_assetCoord").val());
          btn.setAttribute('data-content','<p class="text-muted">لورم ایپسوم متن ساختگی</p>                                <p class="text-primary">لورم ایپسوم متن ساختگی</p>                                <p class="text-success">لورم ایپسوم متن ساختگی</p>                                <p class="text-info">لورم ایپسوم متن ساختگی</p>                                <p class="text-warning">لورم ایپسوم متن ساختگی</p>                                <p class="text-danger">لورم ایپسوم متن ساختگی</p>                        ');
                    btn.setAttribute('data-toggle','popover');
          btn.setAttribute('data-placement','left');
          ibut.classList.add("fa");
          ibut.classList.add("fa-warning");
          $("[data-toggle=popover]")
          .popover({html:true});
          btn.addEventListener("click", function(e){
            // alert();
            // console.log(form.serialize());
          });


         // console.log(data.html_maintenanceType_list);
        }
        else {

          $("#company-table tbody").html(data.html_maintenanceType_list);
          $("#modal-company .modal-content").html(data.html_maintenanceType_form);

        }
      }
    });
    return false;

  }


$("#modal-company").on("submit", ".js-assetCad-create-form", saveForm);

});
