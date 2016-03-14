/**
 * Created by Julio on 09-Mar-16.
 */


function keyDownEvt(e) {
    var keyCode = e.which;
    console.log(e.which);
    if (keyCode == 46)
        delCategoria();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        gestCategoria("add");
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        gestCategoria("mod");
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

function gestCategoria(action) {
    show_panel = true;
    if (action == "add") {
        panel_title = "Adicionar categor&iacute;a";
        load_msg = "Adicionando categor&iacute;a...";
    } else {
        panel_title = "Modificar categor&iacute;a";
        load_msg = "Modificando categor&iacute;a...";
        if ($("li a[action=mod-categoria]").parent().hasClass("disabled"))
            show_panel = false;
    }
    cleanData("form", "tabla-categoria");
    updateRecords("tabla-categoria");
    $("#form-categoria-label").html(panel_title);
    if (show_panel)
        $("#form-categoria").modal().on('shown.bs.modal', function () {
            $("#form-categoria input[name=codigo]").focus();
        });
    $("#form-categoria button[type=submit]").click(function () {
        $("#form-categoria").hide();
        loadMask({
            msg: load_msg
        })
    })


}