document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("entry_photo", document.getElementById("file").files[0]);
    const messageElement = document.getElementById('message');

    try {
        // Отримуємо токен доступу з localStorage
        const token = localStorage.getItem('access_token');

        if (!token) {
            messageElement.innerText = 'User is not authenticated';
            messageElement.style.color = 'red';
            messageElement.style.display = 'block';
            return;
        }

        const response = await fetch('/entry_photo/upload-entry-photo', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Обробляємо успішну відповідь
            messageElement.innerText = `Фото завантажено успішно. Дата: ${data.date}, Номерний знак: ${data.license_plate}`;
            messageElement.style.color = 'green';
        } else {
            // Обробляємо помилку
            messageElement.innerText = data.error || 'Помилка завантаження фото';
            messageElement.style.color = 'red';
        }
        messageElement.style.display = 'block';

        // Очищаємо форму
        document.getElementById("file").value = "";
    } catch (error) {
        console.error('Помилка:', error);
        messageElement.innerText = 'Помилка завантаження фото';
        messageElement.style.color = 'red';
        messageElement.style.display = 'block';
    }
});
