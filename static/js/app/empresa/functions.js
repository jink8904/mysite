/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delCategoria();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addCategoria();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modCategoria();
    }
}


function delCategoria() {
    if (!$('li a[action=del-categoria]').parent().hasClass("disabled"))
        swal({
            title: "Eliminar categor&iacute;a",
            text: "Est&aacute; seguro que quiere elimnar la categor&iacute;a seleccionada.",
            html: true,
            showCancelButton: true,
            confirmButtonColor: "#2196F3"
        }, function (ok) {
            if (ok) {
                loadMask({
                    msg: "Eliminando categor&iacute;a..."
                })
                //var tabla_categoria = $("#tabla-categoria").data('dynatable');
                var id = $("#tabla-categoria>tbody>tr.active>td[key=id]").html();
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
                        $(location).attr("href", "/categorias");
                    }
                })
            }
        });
}

function addCategoria() {
    disabled = $("li a[action=mod-categoria]").parent().hasClass("disabled");
    cleanData("form", "tabla-categoria");
    panel_title = "Adicionar categor&iacute;a";
    load_msg = "Adicionando categor&iacute;a...";

    $("#form-categoria-label").html(panel_title);
    $("#form-categoria").modal().on('shown.bs.modal', function () {
        $("#form-categoria input[name=codigo]").focus();
    });

    submitForm("#form-categoria form", function () {
        $("#form-categoria").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modCategoria() {
    cleanData("form", "tabla-categoria");
    updateRecords("tabla-categoria");
    panel_title = "Modificar categor&iacute;a";
    load_msg = "Modificando categor&iacute;a...";

    $("#form-categoria-label").html(panel_title);
    $("#form-categoria").modal().on('shown.bs.modal', function () {
        $("#form-categoria input[name=codigo]").focus();
    });

    submitForm("#form-categoria form", function () {
        $("#form-categoria").hide();
        loadMask({
            msg: load_msg
        })
    });
}