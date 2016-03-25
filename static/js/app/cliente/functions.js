/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delCliente();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addCliente();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modCliente();
    }
}


function delCliente() {
    if (!$('li a[action=del-cliente]').parent().hasClass("disabled")) {
        title = "Eliminar cliente";
        text = "Est&aacute; seguro que quiere eliminar el cliente seleccionado.";
        notificacion(title, text, {
            ok: function () {
                loadMask({
                    msg: "Eliminando cliente..."
                })

                var id = $("#tabla-cliente>tbody>tr.active>td[key=id]").html();
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
                        $(location).attr("href", "/cliente");
                    }
                })
            }
        })
    }
}

function addCliente() {
    cleanData("form", "tabla-cliente");
    panel_title = "Adicionar cliente";
    load_msg = "Adicionando cliente...";

    $("#form-cliente-label").html(panel_title);
    $("#form-cliente").modal().on('shown.bs.modal', function () {
        $("#form-cliente input[name=nombre]").focus();
    });

    submitForm("#form-cliente form", function () {
        $("#form-cliente").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modCliente() {
    if (!$('li a[action=del-cliente]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-cliente");
        updateRecords("tabla-cliente");
        panel_title = "Modificar cliente";
        load_msg = "Modificando cliente...";

        $("#form-cliente-label").html(panel_title);
        $("#form-cliente").modal().on('shown.bs.modal', function () {
            $("#form-cliente input[name=nombre]").focus();
        });

        submitForm("#form-cliente form", function () {
            $("#form-cliente").hide();
            loadMask({
                msg: load_msg
            })
        });
    }
}