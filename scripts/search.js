document.getElementById('findParkingForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const licensePlate = document.getElementById('licensePlate').value;
    const message = document.getElementById('message');
    const outputDiv = document.getElementById('output');

    fetch('/vehicle_search/find-parking-sessions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ license_plate: licensePlate })
    })
    .then(response => {
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return response.json();
    })
    .then(data => {
        console.log('Success:', data);

        // Очистити попередні дані у випадку успішного виконання
        outputDiv.innerHTML = '';
        message.style.display = 'none'; // Приховати блок з повідомленням про помилку

        if (data.parking_sessions && data.parking_sessions.length > 0) {
            // Створення таблиці для парковальних сесій
            const sessions = data.parking_sessions;
            const table = document.createElement('table');
            table.classList.add('parking-sessions-table'); // Додати клас для стилізації

            // Створення заголовків таблиці (th)
            const headers = ["ID", "License Plate", "Owner", "Entry Time", "Exit Time", "Payment Status", "Amount Due", "Is Registered"];
            const headerRow = document.createElement('tr');
            headers.forEach(headerText => {
                const header = document.createElement('th');
                header.textContent = headerText;
                headerRow.appendChild(header);
            });
            table.appendChild(headerRow);

            // Додавання даних у таблицю (td)
            sessions.forEach(session => {
                const row = document.createElement('tr');
                const cellData = [
                    session.id,
                    session.vehicle_id,
                    session.user_id,
                    session.entry_time,
                    session.exit_time,
                    session.payment_status,
                    session.amount_due,
                    session.is_registered
                ];
                cellData.forEach(cellText => {
                    const cell = document.createElement('td');
                    cell.textContent = cellText;
                    row.appendChild(cell);
                });
                table.appendChild(row);
            });

            outputDiv.appendChild(table); // Додати таблицю до блоку виводу
        } else {
            // Якщо не знайдено парковальних сесій або невірний номер
            outputDiv.innerHTML = ''; // Очистити вміст outputDiv перед відображенням повідомлення
            message.innerText = `No parking sessions found for license plate '${licensePlate}'`;
            message.style.display = 'block'; // Показати повідомлення про невірний номер
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        message.innerText = 'Find parking sessions failed. Please try again later.';
        message.style.display = 'block'; // Показати блок з повідомленням про помилку
        outputDiv.innerHTML = ''; // Очистити попередні дані
    });
});
