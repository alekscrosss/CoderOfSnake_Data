document.getElementById('upload-exit-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append("exit_photo", document.getElementById("exit_file").files[0]);


    try {
        const response = await fetch('/exit_photo/upload-exit-photo', {
            method: 'POST',
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
