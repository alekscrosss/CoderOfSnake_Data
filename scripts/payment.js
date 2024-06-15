document.getElementById('payment-form').addEventListener('submit', async function(event) {
            event.preventDefault();

            var formData = new FormData();
            formData.append("license_plate", document.getElementById("license_plate").value);
            formData.append("payment_amount", document.getElementById("payment_amount").value);

            try {
                const response = await fetch('/payment/make-payment', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                const messageElement = document.getElementById('message');

                if (response.ok) {
                    messageElement.innerText = `Платіж успішно здійснено. У вас є 15 хвилин для виїзду. Гарного шляху!`;
                    messageElement.style.color = 'green';
                } else {
                    messageElement.innerText = data.error || 'Помилка здійснення платежу';
                    messageElement.style.color = 'red';
                }

                // Clear the form
                document.getElementById("license_plate").value = "";
                document.getElementById("payment_amount").value = "";
            } catch (error) {
                console.error('Error:', error);
                const messageElement = document.getElementById('message');
                messageElement.innerText = 'Помилка здійснення платежу';
                messageElement.style.color = 'red';
            }
});
