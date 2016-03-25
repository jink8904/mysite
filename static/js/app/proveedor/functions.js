/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delProveedor();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addProveedor();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modProveedor();
    }
}


function delProveedor() {
    if (!$('li a[action=del-proveedor]').parent().hasClass("disabled")) {
        title = "Eliminar proveedor";
        text = "Est&aacute; seguro que quiere eliminar el proveedor seleccionado.";
        notificacion(title, text, {
            ok: function () {
                loadMask({
                    msg: "Eliminando proveedor..."
                })

                var id = $("#tabla-proveedor>tbody>tr.active>td[key=id]").html();
                token = $("input[name=csrfmiddlewaretoken]").attr("value");
                $.ajax({
                    url: "del",
                    method: "post",
                    dataType: 'json',
                    async: true,
                    data: {
                        csrfmiddlewaretoken: token,
                        id: id,
                    },
                    success: function () {
                        $(location).attr("href", "/proveedor");
                    }
                })
            }
        })
    }
}

function addProveedor() {
    cleanData("form", "tabla-proveedor");
    panel_title = "Adicionar proveedor";
    load_msg = "Adicionando proveedor...";

    $("#form-proveedor-label").html(panel_title);
    $("#form-proveedor").modal().on('shown.bs.modal', function () {
        $("#form-proveedor input[name=nombre]").focus();
    });

    submitForm("#form-proveedor form", function () {
        $("#form-proveedor").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modProveedor() {
    if (!$('li a[action=del-proveedor]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-proveedor");
        updateRecords("tabla-proveedor");
        panel_title = "Modificar proveedor";
        load_msg = "Modificando proveedor...";

        $("#form-proveedor-label").html(panel_title);
        $("#form-proveedor").modal().on('shown.bs.modal', function () {
            $("#form-proveedor input[name=nombre]").focus();
        });

        submitForm("#form-proveedor form", function () {
            $("#form-proveedor").hide();
            loadMask({
                msg: load_msg
            })
        });
    }
}