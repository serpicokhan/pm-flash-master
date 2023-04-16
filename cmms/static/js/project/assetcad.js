$(function () {
  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  // JavaScript code to show an image on the canvas and draw a rectangle on click with a textbox and a flag button
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  const img = new Image();
  img.onload = function() {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
  };
  img.src = 'https://www.beneng.co.uk/wp-content/uploads/2015/11/Bennett-Engineering-Design-Solutions-Factory-Layouts-Surveys-Formax-Factory-Plan-2D-CAD.jpg'; // replace with the URL of your image

  let isDrawing = false;
  let startX, startY;
  let textBox;
  let flagBtn = document.getElementById('flag-btn');

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
    console.log(startX,startY,x,y);
    const width = Math.abs(e.offsetX - startX);
    const height = Math.abs(e.offsetY - startY);
    if (width > 0 && height > 0) {
      textBox = document.createElement("textarea");
      textBox.style.position = "relative";
      textBox.style.left = x + "px";
      textBox.style.top = y + "px";
      textBox.style.width = width + "px";
      textBox.style.height = height + "px";
      textBox.addEventListener("change", e => {
        console.log(e.target.value);
      });
      // p=document.getElementById('pcol');
      p=document.getElementById('pcol');
      // p.appendChild(textBox);
      document.body.appendChild(textBox);
      flagBtn.style.display = "block";
      flagBtn.style.position = "relative";
      flagBtn.style.left = x + width - 20 + "px";
      flagBtn.style.top = y + height - 20 + "px";
      document.body.appendChild(flagBtn);
    }
  });

  canvas.addEventListener('click', e => {
    const x = e.offsetX;
    const y = e.offsetY;
    if (textBox && x >= textBox.offsetLeft && x <= textBox.offsetLeft + textBox.offsetWidth &&
        y >= textBox.offsetTop && y <= textBox.offsetTop + textBox.offsetHeight) {
      // alert(textBox.value);
    }
  });




});
