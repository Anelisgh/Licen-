$(document).ready(function() {
  
    $('#NumeAngajatM').change(function() {
        var angajat = $(this).val();
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_cereri?angajat=' + angajat, true);
        xhr.onload = function() {
            if (this.status == 200) {
                var cereri = JSON.parse(this.responseText);
                var select = $('#Cerere');
                select.empty();
                if (cereri.length > 0) {
                    for (var i = 0; i < cereri.length; i++) {
                        var opt = $('<option></option>').attr('value', cereri[i]).text(cereri[i]);
                        select.append(opt);
                    }
                    select.change();
                } else {
                    $('#tipConcediuM').val('');
                    $('#dataCerereM').val('');
                    $('#dataInceputM').val('');
                    $('#dataSfarsitM').val('');
                    $('#eliberatDeM').val('');
                    $('#diagnosticM').val('');
                    $('#accidentMuncaM').val('');
                }
            }
        }
        xhr.send();
    });
    
    $('#NumeAngajatS').change(function() {
        var angajat = $(this).val();
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_cereri?angajat=' + angajat, true);
        xhr.onload = function() {
            if (this.status == 200) {
                var cereri = JSON.parse(this.responseText);
                var select = $('#dataCerere');
                select.empty();
                if (cereri.length > 0) {
                    for (var i = 0; i < cereri.length; i++) {
                        var opt = $('<option></option>').attr('value', cereri[i]).text(cereri[i]);
                        select.append(opt);
                    }
                } else {
                    $('#dataCerere').val('');
                }
            }
        }
        xhr.send();
    });    
    
    $('#Cerere').change(function() {
        var angajat = $('#NumeAngajatM').val();
        var cerere = $(this).val();
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_date_cerere?angajat=' + angajat + '&cerere=' + cerere, true);
        xhr.onload = function() {
            if (this.status == 200) {
                var date_cerere = JSON.parse(this.responseText);
                $('#tipConcediuM').val(date_cerere['tipConcediu']);
                $('#dataCerereM').val(date_cerere['dataCerere']);
                $('#dataInceputM').val(date_cerere['dataInceput']);
                $('#dataSfarsitM').val(date_cerere['dataSfarsit']);
                $('#eliberatDeM').val(date_cerere['eliberatDe']);
                $('#diagnosticM').val(date_cerere['diagnostic']);
                $('#accidentMuncaM').val(date_cerere['accidentMunca']);
            }
        }
        xhr.send();
    });
    
// Pentru ca  formularul de adaugare a unui nou angajat sa aiba toate campurile importante complete
document.getElementById('adaugareConcedii').addEventListener('submit', function(e) {
    var angajat = document.getElementById('NumeAngajatA');
    var tipConcediu = document.getElementById('tipConcediuA');
    var dataCerere = document.getElementById('dataCerereA');
    var deLa = document.getElementById('dataInceputA');
    var panaLa = document.getElementById('dataSfarsitA');
    var eliberatDe = document.getElementById('eliberatDeA');
    var diagnostic = document.getElementById('diagnosticA');
    var accidentMunca = document.getElementById('accidentMuncaA');

    var invalid = false; // verificam daca exista campuri necompletate

    [angajat, tipConcediu, dataCerere, deLa, panaLa, eliberatDe, diagnostic, accidentMunca].forEach(function(input) {
        input.classList.remove('invalid');
    });

    // daca toate inputurile sunt completate
    if (!angajat.value || !tipConcediu.value || !dataCerere.value || !deLa.value || !panaLa.value) {
        e.preventDefault(); // anuleaza trimiterea formularului

        // se adauga clasa 'invalid' la inputurile care nu sunt completate
        [angajat, tipConcediu, dataCerere, deLa, panaLa].forEach(function(input) {
            if (!input.value) {
                input.classList.add('invalid');
                invalid = true;
            }
        });
    }

    // daca inputurile sunt completate doar cand tipConcediu este 'Medical'
    if (tipConcediu.value === 'Medical') {
        if (!eliberatDe.value || !diagnostic.value || !accidentMunca.value) {
            e.preventDefault(); // anuleaza trimiterea formularului

            // se adauga clasa 'invalid' la inputurile care nu sunt completate
            [eliberatDe, diagnostic, accidentMunca].forEach(function(input) {
                if (!input.value) {
                    input.classList.add('invalid');
                    invalid = true;
                }
            });
        }
    }

    if (invalid) {
        e.preventDefault(); 
        alert('Câmpurile obligatorii sunt necompletate!');
    }
    });
});

