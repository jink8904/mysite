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
}

//------------------------ fachao del validator.js ---------------------------------------------

var showErrors = function (selector, msg) {
    if ($(selector).hasClass("tooltipstered"))
        $(selector).tooltipster("destroy");
    $(selector).tooltipster({
        content: msg,
        position: "bottom",
        theme: "tooltipster-error",
    });
    $(selector).addClass("invalid");
    $(selector).focusin(function () {
        $(selector).removeClass("invalid");
        $(selector).tooltipster("disable");
    })
    return false;
}
//---------------------------------------------------------------------
function updateProductsData(th) {
    var selected = $(th).find("option:selected").val();
    var stock = $(th).children("[value=" + selected + "]").attr("stock")
    $("#datos-producto-entrada [name=codigo]").val(selected).selectpicker("refresh")
    $("#datos-producto-entrada [name=producto]").val(selected).selectpicker("refresh")
    $("#datos-producto-entrada [name=stock]").val(stock)
}

function updateComprobantData(th) {
    var selected = $(th).find("option:selected").val();
    $("#datos-comprobante-entrada [name=identificador]").val(selected).selectpicker("refresh")
    $("#datos-comprobante-entrada [name=nombre]").val(selected).selectpicker("refresh")
}

function addCompra() {
    $("#registro_entradas").removeClass("active")
    $("#detalles_comprobante_compra").addClass("active")
    $("a[href=#registro_entradas]").parent().removeClass("active")
    $("a[href=#detalles_comprobante_compra]").parent().addClass("active")
}


var llenarDatosImportesCompra = function (prod_id) {
    var result = true;
    var igv = $("#datos-producto-entrada input[name=igv]").val();
    if ($("#datos-producto-entrada [name=igv-checkbox]").val() == 'off')
        igv = 0

    var cant = $("#datos-producto-entrada input[name=cantidad]").val(),
        valor_unitario = parseFloat($("#importes-unitarios-entrada input[name=valor-unitario]").val()),
        igv_unitario = igv / 100 * valor_unitario,
        precio_unitario = igv_unitario + valor_unitario,
        valor_compra = cant * valor_unitario,
        igv_total = cant * igv_unitario,
        precio_compra = valor_compra + igv_total;

    detalle_compra_actual = {
        cant: parseInt(cant),
        valor_unitario: parseFloat(valor_unitario).toFixed(2),
        igv: parseFloat(igv).toFixed(2),
        igv_unitario: igv_unitario.toFixed(2),
        precio_unitario: precio_unitario.toFixed(2),
        valor_compra: valor_compra.toFixed(2),
        igv_total: igv_total.toFixed(2),
        precio_compra: precio_compra.toFixed(2)
    }
    if (prod_id == 0 || !cant || !valor_unitario) {
        result = false
        var select_cod = "#datos-producto-entrada [name=codigo]";
        var select_prod = "#datos-producto-entrada [name=producto]";
        if (prod_id == 0) {
            $(select_cod).next().children(":first").addClass("invalid");
            $(select_cod).change(function () {
                //var selected = $(this).find("option:selected").val();
                if ($(select_cod).next().children(":first").hasClass("invalid")) {
                    $(select_cod).next().children(":first").removeClass("invalid")
                    $(select_prod).next().children(":first").removeClass("invalid")
                }
            })
            $(select_prod).next().children(":first").addClass("invalid");
            $(select_prod).change(function () {
                //var selected = $(this).find("option:selected").val();
                if ($(select_prod).next().children(":first").hasClass("invalid")) {
                    $(select_cod).next().children(":first").removeClass("invalid")
                    $(select_prod).next().children(":first").removeClass("invalid")
                }
            })
        }

        if (!valor_unitario) {
            var sel_valor_unitario = "#importes-unitarios-entrada input[name=valor-unitario]";
            showErrors(sel_valor_unitario, "El campo es requerido")
        }

        if (!cant) {
            var sel_cantidad = "#datos-producto-entrada input[name=cantidad]";
            showErrors(sel_cantidad, "El campo es requerido")
        }
    } else {
        $("#importes-unitarios-entrada input[name=valor-unitario]").val(valor_unitario.toFixed(2))
        $("#importes-unitarios-entrada input[name=igv-unitario]").val(igv_unitario.toFixed(2));
        $("#importes-unitarios-entrada input[name=precio-unitario]").val(precio_unitario.toFixed(2));
        $(" #importes-totales-entrada input[name=valor-compra]").val(valor_compra.toFixed(2));
        $("#importes-totales-entrada input[name=igv-total]").val(igv_total.toFixed(2));
        $("#importes-totales-entrada input[name=precio-compra]").val(precio_compra.toFixed(2));
    }
    return result;
}

detalle_compra_list = {};
var addDetalleCompra = function () {
    var prod_id = $("#datos-producto-entrada [name=codigo]").val();
    no_error = llenarDatosImportesCompra(prod_id);
    if (no_error && detalle_compra_actual) {
        var codigo = $("#datos-producto-entrada [name=codigo] option[value=" + prod_id + "]").html();
        var producto = $("#datos-producto-entrada [name=producto] option[value=" + prod_id + "]").html();
        detalle_compra_list[prod_id] = detalle_compra_actual;
        var det = '<tr>' +
            '<td name="id" class="hidden">' + prod_id + '</td>' +
            '<td name="codigo">' + codigo + '</td>' +
            '<td name="producto">' + producto + '</td>' +
            '<td name="cantidad">' + detalle_compra_actual.cant + '</td>' +
            '<td name="valor_unitario">' + detalle_compra_actual.valor_unitario + '</td>' +
            '<td name="valor_compra">' + detalle_compra_actual.valor_compra + '</td>' +
            '<td name="igv_total">' + detalle_compra_actual.igv_total + '</td>' +
            '<td name="precio_compra">' + detalle_compra_actual.precio_compra + '</td>' +
            '</tr>'
        $("#tabla-detalle-compra").removeClass("hidden");
        $(det).appendTo("#tabla-detalle-compra>tbody").click(function (ev) {
            cleanData("table", "tabla-detalle-compra");
            $(this).addClass("active");
            $("#del-detalle-compra").removeClass("disabled");
        });
        limpiarCamposAddDet("entrada");
    }
}

var eliminarDetalleCompra = function () {
    var record = getRecord("tabla-detalle-compra");
    delete detalle_compra_list[record.id]
    console.log(detalle_compra_list);
    $("#tabla-detalle-compra>tbody>tr.active").remove();
}

var validateSalidaMercancia = function () {
    var result = true;
    var tipo_comprobante = "#datos-comprobante-entrada [name=tipo-comprobante]"
    var identificador = "#datos-comprobante-entrada [name=identificador]"
    var nombre = "#datos-comprobante-entrada [name=nombre]"
    var fecha = "#datos-comprobante-entrada [name=fecha]"
    var serie = "#datos-comprobante-entrada [name=serie]"
    var numero = "#datos-comprobante-entrada [name=numero]"
    if ($(tipo_comprobante).val() == 0) {
        $(tipo_comprobante).next().children(":first").addClass("invalid");
        $(tipo_comprobante).change(function () {
            //var selected = $(this).find("option:selected").val();
            if ($(tipo_comprobante).next().children(":first").hasClass("invalid")) {
                $(tipo_comprobante).next().children(":first").removeClass("invalid")
            }
        })
        result = false
    }
    if ($(nombre).val() == 0) {
        $(nombre).next().children(":first").addClass("invalid");
        $(identificador).next().children(":first").addClass("invalid");
        $(nombre).change(function () {
            //var selected = $(this).find("option:selected").val();
            if ($(nombre).next().children(":first").hasClass("invalid")) {
                $(nombre).next().children(":first").removeClass("invalid")
                $(identificador).next().children(":first").removeClass("invalid")
            }
        })
        $(identificador).change(function () {
            //var selected = $(this).find("option:selected").val();
            if ($(identificador).next().children(":first").hasClass("invalid")) {
                $(nombre).next().children(":first").removeClass("invalid")
                $(identificador).next().children(":first").removeClass("invalid")
            }
        })
        result = false
    }

    if ($(fecha).val() == "") {
        showErrors(fecha, "Campo requerido");
        result = false
    }

    if ($(serie).val() == "") {
        showErrors(serie, "Campo requerido");
        result = false
    }

    if ($(numero).val() == "") {
        showErrors(numero, "Campo requerido");
        result = false
    }
    if ($.isEmptyObject(detalle_compra_list)) {
        var msg = "No existen detalles de compra.";
        showMsg(msg, "error", {
            duration: 100
        });
        result = false
    }
    return result;
}

var addSalidaMercancia = function () {
    var fecha = $("#datos-comprobante-entrada [name=fecha]").val();
    datos_compra = {
        tipo_comprobante: $("#datos-comprobante-entrada [name=tipo-comprobante]").val(),
        fecha: fecha,
        serie: $("#datos-comprobante-entrada [name=serie]").val(),
        numero: $("#datos-comprobante-entrada [name=numero]").val(),
        cliente: $("#datos-comprobante-entrada [name=identificador]").val(),
    }
    token = $("input[name=csrfmiddlewaretoken]").attr("value");
    if (validateSalidaMercancia())
        $.ajax({
            url: "add",
            method: "post",
            dataType: 'json',
            async: true,
            data: {
                csrfmiddlewaretoken: token,
                detalle_compra_list: JSON.stringify(detalle_compra_list),
                datos_compra: JSON.stringify(datos_compra)
            },
            success: function (data) {
                $(location).attr("href", "/entrada");
            }
        })
}

var verDetallesCompra = function () {
    var compra = getRecord("tabla-compras");
    token = $("input[name=csrfmiddlewaretoken]").attr("value");
    $.ajax({
        url: "detalles",
        method: "post",
        dataType: 'json',
        async: true,
        data: {
            csrfmiddlewaretoken: token,
            id_compra: compra.id,
        },
        success: function (data) {
            $("#tabla-d-compra-modal>tbody>tr").each(function (index, th) {
                $(th).remove();
            })
            detalle_list = data["d_list"]
            for (var i in detalle_list) {
                var detalle = detalle_list[i];
                var det = '<tr>' +
                    '<td name="codigo">' + detalle['codigo'] + '</td>' +
                    '<td name="descripcion">' + detalle['descripcion'] + '</td>' +
                    '<td name="cantidad">' + detalle['cantidad'] + '</td>' +
                    '<td name="valor_unitario">' + parseFloat(detalle['valor_unitario']).toFixed(2) + '</td>' +
                    '<td name="valor_compra">' + parseFloat(detalle['valor_compra']).toFixed(2) + '</td>' +
                    '<td name="igv">' + parseFloat(detalle['igv']).toFixed(2) + '</td>' +
                    '<td name="importe">' + parseFloat(detalle['importe']).toFixed(2) + '</td>' +
                    '</tr>';
                $(det).appendTo("#tabla-d-compra-modal>tbody")
            }
            $("#modal-detalles-compra").modal();
        }
    })
}