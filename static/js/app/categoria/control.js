/**
 * Created by Julio on 13-Mar-16.
 */
$.ready(function () {
    //------------------- Categoria   -------------------
    $("li a[action=add-categoria]").click(function () {
        cleanData("form", "tabla-categoria");
        $("#form-categoria-label").html("Adicionar categor&iacute;a");
        $("#form-categoria").modal();
        $("#form-categoria button[type=submit]").click(function () {
            $("#form-categoria").hide();
            loadMask({
                msg: "Adicionando categor&iacute;a..."
            })
        })
    })

    $("li a[action=del-categoria]").on('click', function () {
        if (!$(this).parent().hasClass("disabled"))
            swal({
                title: "Eliminar categor&iacute;a",
                text: "Est&aacute; seguro que quiere elimnar la categor&iacute;a seleccionada.",
                html: true,
                showCancelButton: true,
                confirmButtonColor: "#2196F3"
            }, function (ok) {
                if (ok)
                    delCategoria();
            });
    });

    $("button[table=tabla-categoria][accion=add]").click(function () {
        cleanData("form", "tabla-categoria");
        $("#form-categoria-label").html("Adicionar categor&iacute;a");
        $("#form-categoria").modal();

    })
    $("button[table=tabla-categoria][accion=mod]").click(function () {
        if (!$(this).hasClass("disabled")) {
            updateRecords("tabla-categoria");
            $("#form-empresa-label").html("Modificar categor&iacute;a");
            $("#form-categoria").modal();
        }
    })
    $("button[table=tabla-categoria][accion=del]").click(function () {
        if (!$(this).hasClass("disabled")) {
            $(".confirm-del").modal();
            var codigo = $("#tabla-categoria tr.active td[key=codigo]").html();
            $("form[accion=del] input[name=codigo]").val(codigo);
        }
    })
})