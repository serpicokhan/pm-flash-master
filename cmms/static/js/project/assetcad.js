$(function () {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  const img = new Image();
  img.onload = function() {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
  };
  // img.src = 'https://via.placeholder.com/800x780.png'; // replace with the URL of your image
  img.src = 'https://th.bing.com/th/id/R.879f9abfa6f951030c10799d2f00149c?rik=zS%2bFqr9767MDKA&pid=ImgRaw&r=0'; // replace with the URL of your image

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

  canvas.addEventListener('mousedown', e => {
    startX = e.offsetX;
    startY = e.offsetY;
    isDrawing = true;
  });

  canvas.addEventListener('mousemove', e => {
    if (!isDrawing) return;
    const currentX = e.offsetX;
    const currentY = e.offsetY;
    const width = currentX - startX;
    const height = currentY - startY;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    ctx.strokeRect(startX, startY, width, height);
  });

  canvas.addEventListener('mouseup', e => {
    isDrawing = false;
    const x = Math.min(startX, e.offsetX);
    const y = Math.min(startY, e.offsetY);
    const width = Math.abs(e.offsetX - startX);
    const height = Math.abs(e.offsetY - startY);
    if (width > 0 && height > 0) {
      textBox = document.createElement("input");
      textBox.type="text"
      textBox.style.position = "absolute";
      textBox.style.left = x + "px";
      textBox.style.top = y + "px";
      textBox.style.width = width + "px";
      textBox.style.height = height + "px";
      textBox.classList.add('advanced2AutoComplete');
      textBox.addEventListener("change", e => {
        console.log(e.target.value);
      });
      textBox.addEventListener('mousedown', startDragging);
      textBox.addEventListener('mouseup', stopDragging);
      pcol=document.getElementById('pcol');
      pcol.appendChild(textBox);

    }
  });

  canvas.addEventListener('click', e => {
    const x = e.offsetX;
    const y = e.offsetY;
    // if (textBox && x >= textBox.offsetLeft && x <= textBox.offsetLeft + textBox.offsetWidth &&
    //     y >= textBox.offsetTop && y <= textBox.offsetTop + textBox.offsetHeight) {
    //   // alert(textBox.value);
    // }
    var rect = canvas.getBoundingClientRect();
    var x1 = event.clientX - rect.left;
    var y1 = event.clientY - rect.top;
    loadForm(x1,y1);


  // Update the modal content with the click position
  // var clickPosition = document.getElementById("clickPosition");
  // clickPosition.innerHTML = "X: " + x1 + ", Y: " + y1;

  });

  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  var loadForm =function (x1,y1) {

    //console.log($(btn).attr("type"));
    //console.log($(btn).attr("data-url"));

    return $.ajax({
      url: '/Asset/Cad/create',
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
        console.log(x1,y1);
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
          .popover({html:true})
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