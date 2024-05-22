var container 
var newGridButton 

var centerX
var centerY

var image

var blockSize = 3

window.onload = function() {
    container = document.querySelector("#container"); 
    //newGridButton = document.querySelector("#new-grid")
    
    container.addEventListener('click', function(event) {
        const canvas = event.target;
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const ctx = canvas.getContext('2d');

        manipulatePixels(ctx, container.width, container.height, x, y)
    });
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
        manipulatePixels(context, img.width, img.height, 0,0)
    };


    console.log('finished')


}

function manipulatePixels(ctx, width, height, x, y) {
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;
    console.log(imageData)

    i = (y * width + x) * 4

    data[i] -= 255
    data[i+1] -= 255


    console.log(imageData)

    ctx.putImageData(imageData, 0, 0)
}

