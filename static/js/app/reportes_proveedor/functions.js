/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addVenta();
    }
    if (keyCode == 68 && e.ctrlKey) {
        e.preventDefault();
        verDetallesVenta()
    }
}

//---------------------------------------------------------------------

function updateClientData(th) {
    var selected = $(th).find("option:selected").val();
    $("#form-reporte-proveedor [name=identificador]").val(selected).selectpicker("refresh")
    $("#form-reporte-proveedor [name=nombre]").val(selected).selectpicker("refresh")
}

function exportarExcel() {
    $(location).attr("href", "/reporte-proveedor/export-excel");
}

function exportarPDF() {
    $(location).attr("href", "/reporte-proveedor/export-pdf");
}
