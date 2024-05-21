function uploadImage() {
    const file = document.getElementById('image').files[0];
    const formData = new FormData();
    console.log(file)
    formData.append('image', file);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });

    window.location.href = "../canvas";
}

