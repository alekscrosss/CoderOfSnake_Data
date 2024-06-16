document.getElementById('upload-exit-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("exit_photo", document.getElementById("exit_file").files[0]);
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


        const response = await fetch('/exit_photo/upload-exit-photo', {
            method: 'POST',
            headers: {

              'Authorization': `Bearer ${token}`,
            },
            body: formData
        });
        const data = await response.json();

        const messageElement = document.getElementById('message');
        if (response.ok) {
            messageElement.innerText = `Вихід.  Фото успішно завантажено. Дата виходу: ${data.exit_time}, Сума до сплати: ${data.amount_due}`;
            messageElement.style.color = 'green';
        } else {
            messageElement.innerText = data.error || 'Error uploading exit photo';
            messageElement.style.color = 'red';

        }

        document.getElementById("exit_file").value = "";

    } catch (error) {
        console.error('Error:', error);
        const messageElement = document.getElementById('message');
        messageElement.innerText = 'Error uploading exit photo';
        messageElement.style.color = 'red';
    }
});
