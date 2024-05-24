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

        const pixelCoordinates = { x: x, y: y };

        fetch('http://localhost:5000/region', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(pixelCoordinates)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from server:', data);

            data.coordinates.forEach(pixel => {
                manipulatePixels(ctx, container.width, container.height, pixel[1], pixel[0], data.color)
            });

        })
        .catch(error => {
            console.error('Error:', error);
        });

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
    };


    console.log('finished')


}

function manipulatePixels(ctx, width, height, x, y, color) {
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;

    i = (y * width + x) * 4

    data[i] = color[2] // Red
    data[i+1] = color[1] // Green
    data[i+2] = color[0] // Blue

    ctx.putImageData(imageData, 0, 0)
}

