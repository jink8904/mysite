/**
 * Created by Julio on 16-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 80 && e.ctrlKey) {
        e.preventDefault();
        exportarPDF()
    }
    if (keyCode == 69 && e.ctrlKey) {
        e.preventDefault();
        exportarExcel()
    }
}


function exportarExcel() {
    $(location).attr("href", "/stock-disponible/export-excel");
}

function exportarPDF() {
    $(location).attr("href", "/stock-disponible/export-pdf");
}