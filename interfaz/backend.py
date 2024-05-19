from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha subido ninguna imagen'}), 400

    image_file = request.files['image']

    # Guardar la imagen en el servidor
    image_name = image_file.filename
    image_file.save('./static/images/image.jpg')

    # Enviar una respuesta JSON con el nombre de la imagen
    return jsonify({'message': f'Imagen subida correctamente: {image_name}'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')
