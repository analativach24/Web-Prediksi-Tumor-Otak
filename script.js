document.getElementById('predict-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("image", document.getElementById('image').files[0]);

    fetch('/api/predict', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())  // Pastikan response diubah menjadi JSON
    .then(data => {
        console.log(data);  // Log response untuk debugging
        if (data.tumor_type) {
            document.getElementById('result').innerText = 'Predicted Tumor: ' + data.tumor_type;
        } else {
            document.getElementById('result').innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    });
});

// Fungsi untuk mengirim gambar ke server dan menampilkan hasil prediksi
function predictTumor() {
    const fileInput = document.getElementById('image-input');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/api/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction) {
            document.getElementById('prediction-result').innerHTML = `Predicted Tumor: ${data.prediction}`;
        } else {
            document.getElementById('prediction-result').innerHTML = 'Error in prediction';
        }
    })
    .catch(error => {
        document.getElementById('prediction-result').innerHTML = 'Error: ' + error.message;
    });
}
