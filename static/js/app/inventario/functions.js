/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 73 && e.ctrlKey) {
        e.preventDefault();
        addInventario();
    }
}


function addInventario() {
    if (!$('li a[action=add-inventario]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-inventario");
        record = getRecord("tabla-inventario");
        panel_title = "Declarar inventario inicial del producto " + record.nombre;
        load_msg = "Declarando inventario inicial...";

        $("#form-inventario [name=id]").val(record.id);
        $("#inventario-form-title").html(panel_title);
        $("#form-inventario").modal().on('shown.bs.modal', function () {
            $("#form-inventario input[name=cantidad]").focus();
        });

        submitForm("#form-inventario form", function () {
            $("#form-inventario").hide();
            loadMask({
                msg: load_msg
            })
        });

    }
}


function updateInventarioFormData() {
    var costo_unitario = $("#form-inventario [name=costo_unitario]").val();
    var cantidad = $("#form-inventario [name=cantidad]").val();
    if (!isNaN(costo_unitario * cantidad))
        $("#form-inventario [name=costo_total]").val(costo_unitario * cantidad);
    else
        $("#form-inventario [name=costo_total]").val("error");

}