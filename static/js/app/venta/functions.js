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
    $("#datos-producto-salida [name=codigo]").val(selected).selectpicker("refresh")
    $("#datos-producto-salida [name=producto]").val(selected).selectpicker("refresh")
    $("#datos-producto-salida [name=stock]").val(stock)
}

function updateComprobantData(th) {
    var selected = $(th).find("option:selected").val();
    $("#datos-comprobante-salida [name=identificador]").val(selected).selectpicker("refresh")
    $("#datos-comprobante-salida [name=nombre]").val(selected).selectpicker("refresh")
}

function addVenta() {
    $("#registro_salidas").removeClass("active")
    $("#detalles_comprobante_venta").addClass("active")
    $("a[href=#registro_salidas]").parent().removeClass("active")
    $("a[href=#detalles_comprobante_venta]").parent().addClass("active")
}


var llenarDatosImportesVenta = function (prod_id) {
    var result = true;
    var igv = $("#datos-producto-salida input[name=igv]").val();
    if ($("#datos-producto-salida [name=igv-checkbox]").val() == 'off')
        igv = 0

    var cant = $("#datos-producto-salida input[name=cantidad]").val(),
        valor_unitario = parseFloat($("#importes-unitarios-salida input[name=valor-unitario]").val()),
        igv_unitario = igv / 100 * valor_unitario,
        precio_unitario = igv_unitario + valor_unitario,
        valor_venta = cant * valor_unitario,
        igv_total = cant * igv_unitario,
        precio_venta = valor_venta + igv_total;

    detalle_venta_actual = {
        cant: parseInt(cant),
        valor_unitario: parseFloat(valor_unitario).toFixed(2),
        igv: parseFloat(igv).toFixed(2),
        igv_unitario: igv_unitario.toFixed(2),
        precio_unitario: precio_unitario.toFixed(2),
        valor_venta: valor_venta.toFixed(2),
        igv_total: igv_total.toFixed(2),
        precio_venta: precio_venta.toFixed(2)
    }
    if (prod_id == 0 || !cant || !valor_unitario) {
        result = false
        var select_cod = "#datos-producto-salida [name=codigo]";
        var select_prod = "#datos-producto-salida [name=producto]";
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
            var sel_valor_unitario = "#importes-unitarios-salida input[name=valor-unitario]";
            showErrors(sel_valor_unitario, "El campo es requerido")
        }

        if (!cant) {
            var sel_cantidad = "#datos-producto-salida input[name=cantidad]";
            showErrors(sel_cantidad, "El campo es requerido")
        }
    } else {
        $("#importes-unitarios-salida input[name=valor-unitario]").val(valor_unitario.toFixed(2))
        $("#importes-unitarios-salida input[name=igv-unitario]").val(igv_unitario.toFixed(2));
        $("#importes-unitarios-salida input[name=precio-unitario]").val(precio_unitario.toFixed(2));
        $(" #importes-totales-salida input[name=valor-venta]").val(valor_venta.toFixed(2));
        $("#importes-totales-salida input[name=igv-total]").val(igv_total.toFixed(2));
        $("#importes-totales-salida input[name=precio-venta]").val(precio_venta.toFixed(2));
    }
    return result;
}

detalle_venta_list = {};
var addDetalleVenta = function () {
    var prod_id = $("#datos-producto-salida [name=codigo]").val();
    no_error = llenarDatosImportesVenta(prod_id);
    if (no_error && detalle_venta_actual) {
        var codigo = $("#datos-producto-salida [name=codigo] option[value=" + prod_id + "]").html();
        var producto = $("#datos-producto-salida [name=producto] option[value=" + prod_id + "]").html();
        detalle_venta_list[prod_id] = detalle_venta_actual;
        var det = '<tr>' +
            '<td name="codigo">' + codigo + '</td>' +
            '<td name="producto">' + producto + '</td>' +
            '<td name="cantidad">' + detalle_venta_actual.cant + '</td>' +
            '<td name="valor_unitario">' + detalle_venta_actual.valor_unitario + '</td>' +
            '<td name="valor_venta">' + detalle_venta_actual.valor_venta + '</td>' +
            '<td name="igv_total">' + detalle_venta_actual.igv_total + '</td>' +
            '<td name="precio_venta">' + detalle_venta_actual.precio_venta + '</td>' +
            '</tr>'
        $("#tabla-detalle-venta").removeClass("hidden");
        $(det).appendTo("#tabla-detalle-venta>tbody").click(function (ev) {
            cleanData("table", "tabla-detalle-venta");
            $(this).addClass("active");
            $("#del-detalle-venta").removeClass("disabled");
        });
        limpiarCamposAddDet("salida");
    }
}

var eliminarDetalleVenta = function () {
    $("#tabla-detalle-venta>tbody>tr.active").remove();
}

var validateSalidaMercancia = function () {
    var result = true;
    var tipo_comprobante = "#datos-comprobante-salida [name=tipo-comprobante]"
    var identificador = "#datos-comprobante-salida [name=identificador]"
    var nombre = "#datos-comprobante-salida [name=nombre]"
    var fecha = "#datos-comprobante-salida [name=fecha]"
    var serie = "#datos-comprobante-salida [name=serie]"
    var numero = "#datos-comprobante-salida [name=numero]"
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

    if($(fecha).val()==""){
        showErrors(fecha, "Campo requerido");
        result = false
    }

    if($(serie).val()==""){
        showErrors(serie, "Campo requerido");
        result = false
    }

    if($(numero).val()==""){
        showErrors(numero, "Campo requerido");
        result = false
    }


    return result;
}

var addSalidaMercancia = function () {
    var fecha = $("#datos-comprobante-salida [name=fecha]").val();
    datos_venta = {
        tipo_comprobante: $("#datos-comprobante-salida [name=tipo-comprobante]").val(),
        fecha: fecha,
        serie: $("#datos-comprobante-salida [name=serie]").val(),
        numero: $("#datos-comprobante-salida [name=numero]").val(),
        cliente: $("#datos-comprobante-salida [name=identificador]").val(),
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
                detalle_venta_list: JSON.stringify(detalle_venta_list),
                datos_venta: JSON.stringify(datos_venta)
            },
            success: function (data) {
                $(location).attr("href", "/salida");
            }
        })
}

var verDetallesVenta = function () {
    var venta = getRecord("tabla-ventas");
    token = $("input[name=csrfmiddlewaretoken]").attr("value");
    $.ajax({
        url: "detalles",
        method: "post",
        dataType: 'json',
        async: true,
        data: {
            csrfmiddlewaretoken: token,
            id_venta: venta.id,
        },
        success: function (data) {
            $("#tabla-d-venta-modal>tbody>tr").each(function (index, th) {
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
                    '<td name="valor_venta">' + parseFloat(detalle['valor_venta']).toFixed(2) + '</td>' +
                    '<td name="igv">' + parseFloat(detalle['igv']).toFixed(2) + '</td>' +
                    '<td name="importe">' + parseFloat(detalle['importe']).toFixed(2) + '</td>' +
                    '</tr>';
                $(det).appendTo("#tabla-d-venta-modal>tbody")
            }
            $("#modal-detalles-venta").modal();
        }
    })
}