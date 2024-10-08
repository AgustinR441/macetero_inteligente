window.onload = function () {

    function loadData() {
        fetch('/get-data', { cache: 'no-cache' })
            .then(response => response.json())
            .then(data => {
                // Convertir fecha y hora a objeto Date y agregarlo al objeto
                data.forEach(item => {
                    const dateTimeStr = `${item[4]} ${item[5]}`;
                    item.dateObj = new Date(dateTimeStr);
                });

                // Ordenar los datos en orden descendente para la tabla (más reciente primero)
                const tableData = [...data].sort((a, b) => b.dateObj - a.dateObj);

                // Ordenar los datos en orden ascendente para el gráfico (más antiguo primero)
                const chartData = [...tableData].sort((a, b) => a.dateObj - b.dateObj);

                // Actualizar la tabla y el gráfico
                updateTable(tableData);
            });
    }

    function updateTable(data) {
        const tableBody = document.querySelector('tbody');
        tableBody.innerHTML = '';

        data.forEach(item => {
            const row = document.createElement('tr');

            const idCell = document.createElement('td');
            idCell.textContent = item[0];
            row.appendChild(idCell);

            const tempCell = document.createElement('td');
            tempCell.textContent = item[1];
            row.appendChild(tempCell);

            const humedadUpCell = document.createElement('td');
            humedadUpCell.textContent = item[2];
            row.appendChild(humedadUpCell);

            const humedadSubCell = document.createElement('td');
            humedadSubCell.textContent = item[3];
            row.appendChild(humedadSubCell);

            const fechaCell = document.createElement('td');
            fechaCell.textContent = item[4];
            row.appendChild(fechaCell);

            const horaCell = document.createElement('td');
            horaCell.textContent = item[5];
            row.appendChild(horaCell);

            tableBody.appendChild(row);
        });
    }
    loadData();
    setInterval(loadData, 2000);
}
