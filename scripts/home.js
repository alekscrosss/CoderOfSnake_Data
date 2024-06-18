document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/auth/me', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.role === 'admin') {
            document.getElementById('adminReports').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
    });
});

document.getElementById('allDataBtn').addEventListener('click', () => {
    fetch('/reports/reports/make-admin-reports-all_data/', {
        method: 'POST'
    })
    .then(response => response.blob())
    .then(blob => blob.text())
    .then(csvText => {
        displayCsvData(csvText);
    })
    .catch(error => {
        document.getElementById('output').textContent = 'Помилка: ' + error;
    });
});

document.getElementById('usersDataBtn').addEventListener('click', () => {
    fetch('/reports/reports/make-admin-reports-users/', {
        method: 'POST'
    })
    .then(response => response.blob())
    .then(blob => blob.text())
    .then(csvText => {
        displayCsvData(csvText);
    })
    .catch(error => {
        document.getElementById('output').textContent = 'Помилка: ' + error;
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
