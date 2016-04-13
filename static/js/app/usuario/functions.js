/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delUsuario();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addUsuario();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modUsuario();
    }
}


function delUsuario() {
    if (!$('li a[action=del-usuario]').parent().hasClass("disabled")) {
        title = "Eliminar usuario";
        text = "Est&aacute; seguro que quiere eliminar el usuario seleccionado.";
        notificacion(title, text, {
            ok: function () {
                loadMask({
                    msg: "Eliminando usuario..."
                })

                var id = $("#tabla-usuario>tbody>tr.active>td[key=id]").html();
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
                        $(location).attr("href", "/usuario");
                    }
                })
            }
        })
    }
}

function addUsuario() {
    cleanData("form", "tabla-usuario");
    panel_title = "Adicionar usuario";
    load_msg = "Adicionando usuario...";

    $("#form-usuario-label").html(panel_title);
    $("#form-usuario").modal().on('shown.bs.modal', function () {
        $("#form-usuario input[name=usuario]").focus();
    });

    submitForm("#form-usuario form", function () {
        $("#form-usuario").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modUsuario() {
    if (!$('li a[action=del-usuario]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-usuario");
        updateRecords("tabla-usuario");
        panel_title = "Modificar usuario";
        load_msg = "Modificando usuario...";

        $("#form-usuario-label").html(panel_title);
        $("#form-usuario").modal().on('shown.bs.modal', function () {
            $("#form-usuario input[name=usuario]").focus();
        });

        submitForm("#form-usuario form", function () {
            $("#form-usuario").hide();
            loadMask({
                msg: load_msg
            })
        });
    }
}