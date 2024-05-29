var container 
var newGridButton 

var centerX
var centerY

var image

var blockSize = 3
var colorNumber = 0
var color_index

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



            if (colorNumber == data.number) {
                const imageData = ctx.getImageData(0, 0, container.width, container.height);
                const img_arr = imageData.data;


                data.coordinates.forEach(pixel => {
                    manipulatePixels(img_arr, container.width, pixel[1], pixel[0], data.color)
                });
                    
                ctx.putImageData(imageData, 0, 0)
            }
            else {
                if (data.number != undefined) {
                    alert('Not the correct color, the correct color is: ' + data.number);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });
}

document.addEventListener('DOMContentLoaded', function() {

    fetch('http://localhost:5000/process', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        displayGrid(data.image)
        displayButtons(data.colors)

        color_index = data.colors
        document.addEventListener('keydown', (event) => {
            const key = event.key;
            if (key >= '0' && key <= '9') {
                updateActiveColor(parseInt(key));
            }
        });

    })
    .catch(error => {
        console.error(error);
    });
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


    document.getElementById('container').classList.remove('hidden');
    console.log('finished')
}

function manipulatePixels(img_array, width, x, y, color) {

    i = (y * width + x) * 4

    img_array[i] = color[2] // Red
    img_array[i+1] = color[1] // Green
    img_array[i+2] = color[0] // Blue

}

function displayButtons(colors) {
    console.log(colors)
    // Get the buttons
    const buttons = [
        document.getElementById('color-0'),
        document.getElementById('color-1'),
        document.getElementById('color-2'),
        document.getElementById('color-3'),
        document.getElementById('color-4'),
        document.getElementById('color-5'),
        document.getElementById('color-6'),
        document.getElementById('color-7'),
        document.getElementById('color-8'),
        document.getElementById('color-9'),
    ];
    
    // Apply the colors to the buttons
    buttons.forEach((button, index) => {
        if (button && colors[index]) {
            button.addEventListener('click', function() {
                updateActiveColor(index);
            });
            const [b, g, r] = colors[index];
            button.style.background = `rgb(${r}, ${g}, ${b})`;
        }
    });
    
    // Make the button container visible
    document.getElementById('color-buttons').classList.remove('hidden');
}

function updateActiveColor(newColorNumber){
    colorNumber = newColorNumber
    console.log(colorNumber)

    const [b, g, r] = color_index[newColorNumber];
    document.body.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
}
