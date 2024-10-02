window.onload = function () {
    let chart;

    function initChart() {
        const ctx = document.getElementById('dataChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Temperatura (°C)',
                        data: [],
                        borderColor: 'rgba(255, 99, 132, 1)',
                        fill: false
                    },
                    {
                        label: 'Humedad Superior (%)',
                        data: [],
                        borderColor: 'rgba(54, 162, 235, 1)',
                        fill: false
                    },
                    {
                        label: 'Humedad Inferior (%)',
                        data: [],
                        borderColor: 'rgba(75, 192, 192, 1)',
                        fill: false
                    }
                ]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'minute',
                            displayFormats: {
                                minute: 'HH:mm'
                            },
                            tooltipFormat: 'yyyy-MM-dd HH:mm:ss'
                        },
                        title: {
                            display: true,
                            text: 'Fecha'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Valores de Sensores'
                        }
                    }
                }
            }
        });
    }

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
                const tableData = [...data].sort((a, b) => b.dateObj - a.dateObj).slice(0, 20);

                // Ordenar los datos en orden ascendente para el gráfico (más antiguo primero)
                const chartData = [...tableData].sort((a, b) => a.dateObj - b.dateObj);

                // Actualizar la tabla y el gráfico
                updateTable(tableData);
                updateChart(chartData);
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

    function updateChart(data) {
        const labels = [];
        const tempData = [];
        const humedadUpData = [];
        const humedadSubData = [];

        data.forEach(item => {
            labels.push(item.dateObj);
            tempData.push(parseFloat(item[1]));
            humedadUpData.push(parseFloat(item[2]));
            humedadSubData.push(parseFloat(item[3]));
        });

        chart.data.labels = labels;
        chart.data.datasets[0].data = tempData;
        chart.data.datasets[1].data = humedadUpData;
        chart.data.datasets[2].data = humedadSubData;
        chart.update();
    }

    initChart();
    loadData();
    setInterval(loadData, 2000);

    document.getElementById('toggleChartBtn').addEventListener('click', function() {
        const chartContainer = $('#chartContainer');
        if (chartContainer.is(':visible')) {
            // Oculta el gráfico con animación
            chartContainer.slideToggle();
            // Cambia la etiqueta del botón a 'Gráficas'
            $(this).text('Ver gráfico');
        } else {
            // Muestra el gráfico con animación
            chartContainer.slideToggle();
            // Cambia la etiqueta del botón a 'Ocultar'
            $(this).text('Ocultar gráfico');
        }
    });
}
