document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    fetch('/api/auth/me', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.role === 'admin') {
            document.getElementById('adminReports').style.display = 'block';
        }
        loadParkingHistory(token);
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
    });
});

function loadParkingHistory(token) {
    fetch('/user/parking_history/', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => response.json())
    .then(data => {
        displayParkingHistory(data);
    })
    .catch(error => {
        console.error('Error fetching parking history:', error);
        document.getElementById('parkingHistoryOutput').textContent = 'Error loading parking history: ' + error;
    });
}

function displayParkingHistory(parkingHistory) {
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');

    const headers = ['Vehicle Number', 'User Name', 'Entry Time', 'Exit Time', 'Payment Status', 'Amount Due', 'Is Registered'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });

    table.appendChild(headerRow);

    parkingHistory.forEach(session => {
        const row = document.createElement('tr');
        const cellValues = [
            session.vehicle_license_plate,
            session.user_name,
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

    const outputDiv = document.getElementById('parkingHistoryOutput');
    outputDiv.innerHTML = '';
    outputDiv.appendChild(table);
}

document.getElementById('allDataBtn').addEventListener('click', () => {
    fetch('/reports/reports/make-admin-reports-all_data/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.blob())
    .then(blob => blob.text())
    .then(csvText => {
        displayCsvData(csvText);
    })
    .catch(error => {
        document.getElementById('output').textContent = 'Error: ' + error;
    });
});

document.getElementById('usersDataBtn').addEventListener('click', () => {
    fetch('/reports/reports/make-admin-reports-users/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.blob())
    .then(blob => blob.text())
    .then(csvText => {
        displayCsvData(csvText);
    })
    .catch(error => {
        document.getElementById('output').textContent = 'Error: ' + error;
    });
});

function displayCsvData(csvText) {
    const rows = csvText.split('\n').map(row => row.split(','));
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');

    rows[0].forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });

    table.appendChild(headerRow);

    rows.slice(1).forEach(rowData => {
        const row = document.createElement('tr');
        rowData.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });
        table.appendChild(row);
    });

    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '';
    outputDiv.appendChild(table);
}
