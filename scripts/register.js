function registerUser() {
    var username = document.getElementById('regUsername').value;
    var email = document.getElementById('regEmail').value;
    var password = document.getElementById('regPassword').value;

    var data = {
        username: username,
        email: email,
        password: password
    };

    fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed. Please try again later.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        var message = document.getElementById('message');
        message.innerText = 'Registration successful. Please check your email for confirmation.';
        message.style.display = 'block'; // Показати повідомлення
        message.style.backgroundColor = '#d4edda'; // Колір успіху
        message.style.borderColor = '#c3e6cb'; // Колір рамки успіху
        message.style.color = '#155724'; // Колір тексту успіху
    })
    .catch((error) => {
        console.error('Error:', error);
        var message = document.getElementById('message');
        if (error.response && error.response.status === 409) {
            message.innerText = 'User with this email already exists.';
        } else {
            message.innerText = 'Registration failed. Please try again later.';
        }
        message.style.display = 'block'; // Показати повідомлення
        message.style.backgroundColor = '#f8d7da'; // Колір помилки
        message.style.borderColor = '#f5c6cb'; // Колір рамки помилки
        message.style.color = '#721c24'; // Колір тексту помилки
    });
}
