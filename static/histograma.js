// PENTRU HISTOGRAMA CONCEDII
fetch('/date_histograma_concedii')
        .then(response => response.json())
        .then(date_histograma_concedii => {
            var nume_luni = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"];
            var luni = Object.keys(date_histograma_concedii).map(luna => nume_luni[luna - 1]); // convertim numerele la nume de luni si scadem una pentru ca "luna" reprezintă numărul lunii returnat de interogarea SQL
            var numar_concedii = Object.values(date_histograma_concedii);
            var ctx = document.getElementById('myChartConcedii').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: luni,
                    datasets: [{
                        label: 'Numarul de concedii pentru fiecare luna',
                        data: numar_concedii,
                        backgroundColor: 'rgba(70, 130, 180, 0.2)',
                        borderColor: 'rgba(70, 130, 180, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: false, // Altfel css-ul nu functioneaza
                    scales: {
                        y: {
                            beginAtZero: true 
                        }
                    }
                }
            });
        });

// Histograma pentru vechime
fetch('/date_histograma_vechime')
.then(response => response.json())
.then(date_histograma_vechime => {
    var vechimi = Object.keys(date_histograma_vechime);
    var numar_angajati = Object.values(date_histograma_vechime);
    var ctx = document.getElementById('myChartVechime').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: vechimi,
            datasets: [{
                label: 'Numarul de angajati in functie de vechime',
                data: numar_angajati,
                backgroundColor: 'rgba(70, 130, 180, 0.2)',
                borderColor: 'rgba(70, 130, 180, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

// Histograma pentru varsta
fetch('/date_histograma_varsta')
.then(response => response.json())
.then(date_histograma_varsta => {
    var varste = Object.keys(date_histograma_varsta);
    var numar_angajati = Object.values(date_histograma_varsta);
    var ctx = document.getElementById('myChartVarsta').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: varste,
            datasets: [{
                label: 'Numarul de angajati pentru fiecare grupa de varsta',
                data: numar_angajati,
                backgroundColor: 'rgba(70, 130, 180, 0.2)',
                borderColor: 'rgba(70, 130, 180, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});