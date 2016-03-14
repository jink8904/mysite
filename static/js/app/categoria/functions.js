/**
 * Created by Julio on 09-Mar-16.
 */
function delCategoria() {
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