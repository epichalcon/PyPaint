document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('image');
    formData.append('image', fileInput.files[0]);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Success: ' + data.message);
            window.location.href = "../canvas";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    });
});
