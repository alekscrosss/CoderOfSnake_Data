document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('message');

    console.log('Submitting login form', { email, password });

    try {
        const response = await fetch('/api/auth/login', {
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
            if (errorData.message === "Invalid email") {
                message.innerText = 'Invalid email. Please try again.';
            } else if (errorData.message === "Email not confirmed") {
                message.innerText = 'Email not confirmed. Please check your email.';
            } else if (errorData.message === "Invalid password") {
                message.innerText = 'Invalid password. Please try again.';
            } else {
                message.innerText = 'Login failed. Please try again later.';
            }
            message.style.display = 'block';
        } else {
            const responseData = await response.json();
            console.log('Login successful');
            // Assuming your backend returns tokens in the response
            localStorage.setItem('access_token', responseData.access_token);
            localStorage.setItem('refresh_token', responseData.refresh_token);
            // Redirect to home.html
            window.location.href = '/home';
        }
    } catch (error) {
        console.error('Error:', error);
        message.innerText = 'Login failed. Please try again later.';
        message.style.display = 'block';
    }
});
