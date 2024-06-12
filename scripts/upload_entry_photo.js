document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append("entry_photo", document.getElementById("file").files[0]);

    try {
        const response = await fetch('/entry_photo/upload-entry-photo', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        const messageElement = document.getElementById('message');

        if (response.ok) {
            // Display success message and recognized license plate number
            messageElement.innerText = `Фото завантажено успішно. Дата: ${data.date}, Номерний знак: ${data.license_plate}`;
            messageElement.style.color = 'green';
        } else {
            messageElement.innerText = data.error || 'Помилка завантаження фото';
            messageElement.style.color = 'red';
        }

        // Clear the form
        document.getElementById("file").value = "";
    } catch (error) {
        console.error('Error:', error);
        const messageElement = document.getElementById('message');
        messageElement.innerText = 'Помилка завантаження фото';
        messageElement.style.color = 'red';
    }
});
