function searchVehicle() {
    const licensePlate = document.getElementById('licensePlate').value.trim();
    console.log("Searching for vehicle:", licensePlate); // Debug info
    fetch('/vehicle_search/find-parking-sessions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ license_plate: licensePlate })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail); });
        }
        return response.json();
    })
    .then(data => {
        console.log("Received data:", data); // Debug info
        displaySearchResults(data.parking_sessions);
    })
    .catch(error => {
        console.error('Error searching for vehicle:', error); // Debug info
        document.getElementById('searchResult').innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    });
}

function displaySearchResults(parkingSessions) {
    const table = document.createElement('table');
    table.classList.add('table', 'table-striped', 'table-bordered');
    const headerRow = document.createElement('tr');

    const headers = ['Vehicle Number', 'User Name', 'Entry Time', 'Exit Time', 'Payment Status', 'Amount Due', 'Is Registered'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });

    table.appendChild(headerRow);

    parkingSessions.forEach(session => {
        const row = document.createElement('tr');
        const cellValues = [
            session.vehicle_id,
            session.user_id,
            session.entry_time,
            session.exit_time || '-',
            session.payment_status,
            session.amount_due !== null ? session.amount_due : '-',
            session.is_registered
        ];

        cellValues.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });
        table.appendChild(row);
    });

    const outputDiv = document.getElementById('searchResult');
    outputDiv.innerHTML = '';
    outputDiv.appendChild(table);
}
