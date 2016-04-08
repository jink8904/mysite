/**
 * Created by Julio on 16-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    console.log(e.which);
    if (keyCode == 80 && e.ctrlKey) {
        e.preventDefault();
        exportarPDF()
    }
    if (keyCode == 69 && e.ctrlKey) {
        e.preventDefault();
        exportarExcel()
    }
    if (keyCode == 68 && e.ctrlKey) {
        e.preventDefault();
        modPeriodo()
    }
}


function exportarExcel() {
    $(location).attr("href", "/reporte-movimientos-productos/export-excel");
}

function exportarPDF() {
    $(location).attr("href", "/reporte-movimientos-productos/export-pdf");
}

function modPeriodo() {
    $(location).attr("href", "/reporte-movimientos-productos");
}

