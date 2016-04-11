/**
 * Created by Julio on 08-Feb-16.
 */
//variables
var empresa_seleccionada = null;

//funciones
keyDownEvt = function () {
};

function showMsg(msg, tipo, opt) {
    var event = new Events();
    var defaults = {
        type: (tipo) ? tipo : 'success',
        duration: 4
    }
    var settings = $.extend({}, defaults, opt);
    if (msg) {
        event.Mensaje(msg, settings);
    }
}

function fixTableSelect() {
    var id = this.id;
    $("#" + id + ">tbody>tr").click(function (evt) {
        var id = $(this).parent().parent().attr("id");
        cleanData('table', id);
        var tr = $(this);
        tr.addClass('active');
        updateButtons(id);
    })
}

function loadMask(options) {
    var defaults = {
        selector: 'body',
        msg: "Cargando..."
    }
    var settings = $.extend({}, defaults, options);

    $(settings.selector).block({
        message: '<span class="text-semibold"><i class="icon-spinner10 spinner"></i><h5>' + settings.msg + '</h5></span>',
        overlayCSS: {
            backgroundColor: '#000000',
            opacity: .5,
            cursor: 'wait',
            position: "fixed",
            zIndex: 1040,
        },
        css: {
            border: 0,
            padding: 0,
            color: '#fff',
            backgroundColor: 'transparent',
            zIndex: 1041,
            position: "fixed",
            fontFamily: 'cursive',
            font: 'initial',
        }
    });
}

function unMask(selector, fn) {
    if (selector == null)
        selector = "body";
    $(selector).unblock({
        onUnblock: fn
    });

}

function notificacion(title, msg, options) {
    var defaults = {
        title: title,
        text: msg,
        confirmButtonColor: "#66BB6A",
        type: "warning",
        allowOutsideClick: !1,
        showConfirmButton: !0,
        showCancelButton: !0,
        closeOnConfirm: !0,
        closeOnCancel: !0,
        confirmButtonText: "Aceptar",
        confirmButtonColor: "#2196F3",
        cancelButtonText: "Cancelar",
        imageUrl: null,
        imageSize: null,
        timer: null,
        customClass: "",
        html: !0,
        animation: !0,
        allowEscapeKey: !0,
        inputType: "text",
        inputPlaceholder: "",
        inputValue: "",
        showLoaderOnConfirm: !1,
        ok: function () {
            console.log("ok")
        },
        cancel: function () {
            console.log("cancel")
        },
    }
    var settings = $.extend({}, defaults, options);
    swal(settings,
        function (ok) {
            if (ok)
                settings.ok();
            else
                settings.cancel();

        }
    );
}

var getRecord = function (table_id) {
    var record = {};
    $("#" + table_id + " tr.active > td").each(function (index, th) {
        var key = "";
        if ($(this).attr("key"))
            key = checkKey($(this).attr("key"));
        else if ($(this).attr("name"))
            key = checkKey($(this).attr("name"));
        record[key] = $(this).html()
    });
    return record;
}

var cleanData = function (tipo, id, callback) {
    switch (tipo) {
        case "table":
            $("#" + id + ">tbody>tr").each(function (index, th) {
                $(this).removeClass('active');
            })
            break;
        case "form":
            var sel = "form[table=" + id + "] input[type!=hidden], form[table=" + id + "] select";
            $(sel).each(function (index, th) {
                $(this).val("");
                $(this).find("option:selected").val("")
                $(this).selectpicker("refresh")
            })
            break;
        case "select":
            $("#" + id + ">option").attr("selected", false);
            if (callback)
                callback();
            break;
    }
}

var checkKey = function (key) {
    switch (key) {
        case "#":
            return "id"
            break;
        case "no_identificacion":
            return "identificador"
            break;
        case "tipo_de_identificacion":
            return "tipo_id"
            break;
    }
    return key;
}

var updateRecords = function (table_id) {
    var record = getRecord(table_id)
    var sel_form = "form[table=" + table_id + "] ";
    //Selecciono el formulario asociado a la tabla pare llenar los campos
    $(sel_form + "input").each(function () {
        var name = $(this).attr("name");
        if (record[name]) {
            $(this).val(record[name]);
        }
    })
    $(sel_form + "select").each(function () {
        var name = $(this).attr("name");
        var record_id = name + "_id";
        var select_id = $(this).attr("id");
        //ta chapusero arreglar despues... nada mas para los bootstrap-select
        $("select[name=" + name + "]").next().children("button").children(".filter-option").html(record[name]);
        $("select[name=" + name + "]").val(record[record_id])
    })
}

var updateButtons = function (table_id) {
    //console.log(table_id);
    var sel_btns = "button[table=" + table_id + "][accion!=add]";
    if (!$(sel_btns).length)
        sel_btns = "li[table=" + table_id + "]";
    $(sel_btns).removeClass("disabled");
}

var updateFooter = function () {
    var empresa = $.parseJSON(sessionStorage.getItem("empresa"));
    var usuario = sessionStorage.getItem("usuario");
    var anno = sessionStorage.getItem("anno");
    var mes = sessionStorage.getItem("mes_mostrar");
    if (empresa) {
        $("#empresa a").html("   " + empresa.nombre);
        $("#barra-menu>ul.hidden").removeClass("hidden");
    } else {
        $("#barra-menu>ul").addClass("hidden");
        $("#barra-menu>ul:first").removeClass("hidden");
    }
    if (usuario)
        $("#usuario a").html("   " + usuario);
    if (mes)
        $("#periodo a").html("   " + mes + ", " + anno);
}


var cambiarComillas = function (obj) {
    var result = '';
    for (var i = 0; i < obj.length; i++) {
        c = obj.charAt(i);
        if (c == "'")
            result += '"'
        else
            result += c;
    }
    return result;
}

var llenarDatosProducto = function (id, selector_id) {
    var productos = $('span[productos]').attr('productos');
    var str = cambiarComillas(productos);
    productos = $.parseJSON(str);
    if (id == 0) {
        $(selector_id + " [name=producto]").val("")
        $(selector_id + " [name=codigo]").val("")
        $(selector_id + " [name=stock]").val("")
    } else {
        $(selector_id + " [name=producto]").val(id)
        $(selector_id + " [name=codigo]").val(id)
        var stock = $(selector_id + " [name=codigo]>option[value=" + id + "]").attr("stock");
        $(selector_id + " [name=stock]").val(stock)

    }

}


detalle_venta_actual = {}
detalle_compra_actual = {}
var limpiarCamposAddDet = function (tipo) {
    $("#datos-producto-" + tipo + " [name=cantidad]").val("");
    $("#importes-unitarios-" + tipo + " input").val("");
    $("#importes-totales-" + tipo + " input").val("");
    detalle_venta_actual = null;
    detalle_compra_actual = null;
}



