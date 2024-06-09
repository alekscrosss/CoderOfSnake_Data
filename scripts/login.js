document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('message');

    console.log('Submitting login form', { email, password });

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'username': email,
                'password': password
            })
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorData = await response.json();
            console.log('Error data:', errorData);
            if (errorData.detail === "Invalid email") {
                message.innerText = 'Invalid email. Please try again.';
            } else if (errorData.detail === "Email not confirmed") {
                message.innerText = 'Email not confirmed. Please check your email.';
            } else if (errorData.detail === "Invalid password") {
                message.innerText = 'Invalid password. Please try again.';
            } else {
                message.innerText = 'Login failed. Please try again later.';
            }
            message.style.display = 'block';
        } else {
            console.log('Login successful');
            window.location.href = '/home';
        }
    } catch (error) {
        console.error('Error:', error);
        message.innerText = 'Login failed. Please try again later.';
        message.style.display = 'block';
    }
});
