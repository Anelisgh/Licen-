document.querySelectorAll('#colorSelector a').forEach(function(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        setTheme(this.dataset.value);
        localStorage.setItem('theme', this.dataset.value);
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        setTheme('default'); 
    }
});

function setTheme(theme) {
    let root = document.documentElement.style;
    switch(theme) {
        case 'albastru':
            root.setProperty('--flash-text', 'white');
            root.setProperty('--flash-background', '#5e5e85');
            root.setProperty('--flash-border', '#4b4b66');
            root.setProperty('--table-shadow', '#454562');
            root.setProperty('--table-border', '#4e4e6e');
            root.setProperty('--table-color-title', '#666690');
            root.setProperty('--table-color-elements', '#70709a');
            root.setProperty('--hover-table', '#565679');
            root.setProperty('--firma', '#35354b');
            root.setProperty('--sidenav', '#565679');
            break;
        case 'verzui':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#d7f0da');
            root.setProperty('--flash-border', '#a4bea3');
            root.setProperty('--table-shadow', '#b7c7bd');
            root.setProperty('--table-border', '#a4bea3');
            root.setProperty('--table-color-title', '#d7f0da');
            root.setProperty('--table-color-elements', '#ecf7ed');
            root.setProperty('--hover-table', '#b0dfb0');
            root.setProperty('--sidenav', '#345e40');
            root.setProperty('--firma', 'black');
            break;
        case 'verde':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#5e8562');
            root.setProperty('--flash-border', '#4e6e51');
            root.setProperty('--table-shadow', '#456248');
            root.setProperty('--table-border', '#4e6e51');
            root.setProperty('--table-color-title', '#66906a');
            root.setProperty('--table-color-elements', '#709a74');
            root.setProperty('--hover-table', '#567959');
            root.setProperty('--firma', '#1a291e');
            root.setProperty('--sidenav', '#567959');
            break;
        case 'rosu':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#b27c84');
            root.setProperty('--flash-border', '#9f5d67');
            root.setProperty('--table-shadow', '#7e4a52');
            root.setProperty('--table-border', '#a96c75');
            root.setProperty('--table-color-title', '#b27c84');
            root.setProperty('--table-color-elements', '#bc8c93');
            root.setProperty('--hover-table', '#9f5d67');
            root.setProperty('--firma', '#6f4148');
            root.setProperty('--sidenav', '#9f5d67');
            break;
        case 'gri':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#c3c3c3');
            root.setProperty('--flash-border', '#929292');
            root.setProperty('--table-shadow', '#a6a6a6');
            root.setProperty('--table-border', '#929292');
            root.setProperty('--table-color-title', '#c3c3c3');
            root.setProperty('--table-color-elements', '#d9d9d9');
            root.setProperty('--hover-table', '#9e9e9e');
            root.setProperty('--sidenav', '#2c2c2c');
            root.setProperty('--firma', 'black');
            break;
/*
        case '':
            root.setProperty('--flash-text', '#');
            root.setProperty('--flash-background', '#');
            root.setProperty('--flash-border', '#');
            root.setProperty('--table-shadow', '#');
            root.setProperty('--table-border', '#');
            root.setProperty('--table-color-title', '#');
            root.setProperty('--table-color-elements', '#');
            root.setProperty('--text-table-title', 'white');
            root.setProperty('--hover-table', '#');
            root.setProperty('--firma', '');
            root.setProperty('--sidenav', '');
            break;
*/
        default:
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#dae6f0');
            root.setProperty('--flash-border', '#a4b0be');
            root.setProperty('--table-shadow', '#bdc3c7');
            root.setProperty('--table-border', '#a4b0be');
            root.setProperty('--table-color-title', '#dae6f0');
            root.setProperty('--table-color-elements', '#ecf2f7');
            root.setProperty('--hover-table', '#b0cadf');
            root.setProperty('--sidenav', '#354b60');
            root.setProperty('--firma', 'black');
            break;
    }
}
function createColorPreview(theme) {
    let colorPreview = document.createElement('div');
    colorPreview.style.position = 'absolute';
    colorPreview.style.right = '-60px'; 
    colorPreview.style.border = '1px solid #ccc';
    colorPreview.style.borderRadius = '4px';
    colorPreview.style.padding = '2px';
    colorPreview.style.backgroundColor = '#f3f3f3';
    colorPreview.style.width = '60px'; 
    colorPreview.style.height = '60px';
    colorPreview.style.display = 'flex'; 
    colorPreview.style.flexDirection = 'row'; 
    colorPreview.style.flexWrap = 'wrap';

    let colors;
    switch(theme) {
        case 'albastru':
            colors = ['#35354b', '#565679', '#666690', '#70709a'];
            break;
        case 'verzui':
            colors = ['#345e40', '#b0dfb0', '#d7f0da', '#ecf7ed'];
            break;
        case 'verde':
            colors = ['#4e6e51', '#567959', '#66906a', '#709a74'];
            break;
        case 'rosu':
            colors = ['#6f4148', '#9f5d67', '#b27c84', '#bc8c93'];
            break;
        case 'gri':
            colors = ['#2c2c2c', '#9e9e9e', '#c3c3c3', '#d9d9d9'];
            break;
        default:
            colors = ['#354b60', '#b0cadf', '#dae6f0', '#ecf2f7'];
    }

    colors.forEach(function(color) {
        let colorBox = document.createElement('div');
        colorBox.style.width = '20px'; 
        colorBox.style.height = '20px'; 
        colorBox.style.backgroundColor = color;
        colorBox.style.margin = '5px';
        colorPreview.appendChild(colorBox);
    });
    return colorPreview;
}

document.querySelectorAll('#colorSelector a').forEach(function(link) {
    link.addEventListener('mouseover', function() {
        let colorPreview = createColorPreview(this.dataset.value);
        this.appendChild(colorPreview);

    });

    link.addEventListener('mouseout', function() {
        this.removeChild(this.lastChild);
    });

    link.addEventListener('click', function(e) {
        e.preventDefault();
        setTheme(this.dataset.value);
        localStorage.setItem('theme', this.dataset.value);
    });
});


function openNav() {
    var mySidenav = document.getElementById("mySidenav");
    var navbutton = document.getElementById("navbutton");
    var tableContainer = document.querySelector(".table-container");
    var myTable = document.getElementById("myTable");
    var myTableC = document.getElementById("myTableC");
    var fieldsets = document.querySelectorAll("fieldset");
    var chart = document.getElementsByClassName("chart");

    if (mySidenav) {
        mySidenav.style.width = "250px";
    }
    if (navbutton) {
        navbutton.style.marginLeft = "250px";
    }
    if (tableContainer) {
        tableContainer.style.marginLeft = "250px";
    }
    if (myTable) {
        myTable.style.marginLeft = "250px";
    }
    if (myTableC) {
        myTableC.style.marginLeft = "650px";
    }
    if (chart) {
        for(var i = 0; i < chart.length; i++) {
            chart[i].style.marginLeft = "250px";
        }
    }
    fieldsets.forEach(function(fieldset) {
        fieldset.style.marginLeft = "250px";
    });
}

function closeNav() {
    var mySidenav = document.getElementById("mySidenav");
    var navbutton = document.getElementById("navbutton");
    var tableContainer = document.querySelector(".table-container");
    var myTable = document.getElementById("myTable");
    var myTableC = document.getElementById("myTableC");
    var fieldsets = document.querySelectorAll("fieldset");
    var chart = document.getElementsByClassName("chart");

    if (mySidenav) {
        mySidenav.style.width = "0";
    }
    if (navbutton) {
        navbutton.style.marginLeft= "0";
    }
    if (tableContainer) {
        tableContainer.style.marginLeft = "0";
    }
    if (myTable) {
        myTable.style.marginLeft = "44px";
    }
    if (myTableC) {
        myTableC.style.marginLeft = "500px";
    }
    if (chart) {
        for(var i = 0; i < chart.length; i++) {
            chart[i].style.marginLeft = "0px";
        }
    }
    fieldsets.forEach(function(fieldset) {
        fieldset.style.marginLeft = "0";
    });
}

// Verificați dacă meniul este deschis sau închis
if (localStorage.getItem('menuStatus') === 'open') {
    openNav();
}

// Actualizați starea meniului atunci când faceți clic pe "open" sau "×"
document.getElementById("mySidenav").getElementsByClassName("closebtn")[0].onclick = function() {
    closeNav();
    localStorage.setItem('menuStatus', 'closed');
}
document.getElementById("navbutton").getElementsByTagName("span")[0].onclick = function() {
    openNav();
    localStorage.setItem('menuStatus', 'open');
}

$(document).ready(function() {
    $("#flashMessage").delay(5000).slideUp(300); });