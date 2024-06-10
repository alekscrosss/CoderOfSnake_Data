document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append("entry_photo", document.getElementById("file").files[0]);
    formData.append("license_plate", document.getElementById("license_plate").value);

    try {
        const response = await fetch('/entry_photo/upload-entry-photo', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();


        if (response.ok) {
            // Вивести повідомлення про успішне завантаження
            const messageElement = document.getElementById('message');
            messageElement.innerText = `Фото завантажено успішно. Дата: ${data.date}, Номерний знак: ${data.license_plate}`;
            messageElement.style.color = 'green';
        } else {
            const messageElement = document.getElementById('message');
            messageElement.innerText = data.error || 'Помилка завантаження фото';
            messageElement.style.color = 'red';
        }

        // Очищення форми
        document.getElementById("file").value = "";
        document.getElementById("license_plate").value = "";
    } catch (error) {
        console.error('Error:', error);
        const messageElement = document.getElementById('message');
        messageElement.innerText = 'Помилка завантаження фото';
        messageElement.style.color = 'red';
    }
});
