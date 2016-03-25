/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delProducto();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addProducto();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modProducto();
    }
}


function delProducto() {
    if (!$('li a[action=del-producto]').parent().hasClass("disabled")) {
        title = "Eliminar producto";
        text = "Est&aacute; seguro que quiere eliminar la producto seleccionado.";
        notificacion(title, text, {
            ok: function () {
                loadMask({
                    msg: "Eliminando producto..."
                })

                var id = $("#tabla-producto>tbody>tr.active>td[key=id]").html();
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
                        $(location).attr("href", "/productos");
                    }
                })
            }
        })
    }
}

function addProducto() {
    cleanData("form", "tabla-producto");
    panel_title = "Adicionar producto";
    load_msg = "Adicionando producto...";

    $("#form-producto-label").html(panel_title);
    $("#form-producto").modal().on('shown.bs.modal', function () {
        $("#form-producto input[name=nombre]").focus();
    });

    submitForm("#form-producto form", function () {
        $("#form-producto").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modProducto() {
    if (!$('li a[action=del-producto]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-producto");
        updateRecords("tabla-producto");
        panel_title = "Modificar producto";
        load_msg = "Modificando producto...";

        $("#form-producto-label").html(panel_title);
        $("#form-producto").modal().on('shown.bs.modal', function () {
            $("#form-producto input[name=nombre]").focus();
        });

        submitForm("#form-producto form", function () {
            $("#form-producto").hide();
            loadMask({
                msg: load_msg
            })
        });
    }
}