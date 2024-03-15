document.getElementById("filetag").addEventListener("change", function(e) {

    let newImg = new Image(width, height);
  
    // Equivalent to above -> let newImg = document.createElement("img");
  
    newImg.src = e.target.files[0];
    newImg.src = URL.createObjectURL(e.target.files[0]);
  
    output.appendChild(newImg);
  });