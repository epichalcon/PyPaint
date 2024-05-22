from flask import Flask, render_template, request, jsonify
from Pypainting import pypainting
from Pypainting.contours import Contour


app = Flask(__name__)

image_name : str | None
regions = {}
centers = []

@app.route('/upload', methods=['POST'])
def upload_image():
    global image_name
    print(request.files)
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha subido ninguna imagen'}), 400

    image_file = request.files['image']

    # Guardar la imagen en el servidor
    image_name = image_file.filename
    image_file.save(f'./static/images/{image_name}')

    print(image_name)
    
    # Enviar una respuesta JSON con el nombre de la imagen
    return jsonify({'message': f'Imagen subida correctamente: {image_name}'})




@app.route('/process', methods=['GET'])
def get_processed_images():
    global image_name
    global regions 
    global centers
    edges, regions, centers = pypainting.main(image_name)
    return jsonify({'image': edges})

@app.route('/region', methods=['POST'])
def get_region_from_pixel():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    coordinates_key = (y, x)
    if coordinates_key in regions:
        contour = regions[coordinates_key]
        print(contour)

        return jsonify({'status': 'success', 'coordinates': list(contour.coords), 'color': list(centers[contour.color])}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Coordinates not found'}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')
