var container 
var newGridButton 

var centerX
var centerY

var image

var blockSize = 3

window.onload = function() {
    container = document.querySelector("#container"); 
    //newGridButton = document.querySelector("#new-grid")
}


fetch('http://localhost:5000/process', {
    method: 'GET',
})
.then(response => response.json())
.then(data => {
    displayGrid(data.image)
})
.catch(error => {
    console.error(error);
});


function displayGrid(imageBase64){
    context = container.getContext("2d")
    const img = new Image();

    img.src = 'data:image/png;base64,' + imageBase64;

    img.onload = function() {
        container.width = img.width;
        container.height = img.height;
        context.drawImage(img, 0, 0);
    };

    console.log('finished')
}
