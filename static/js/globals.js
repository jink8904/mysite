/**
 * Created by Julio on 03-Feb-16.
 */
$(document).ready(function () {
    document.addEventListener("keydown", keyDownEvt, false);
    updateFooter();
    //------------- Configuracion de las tablas -------------
    $("#tabla-empresa").dynatable({
        params: {
            records: "empresas"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-categoria").dynatable({
        params: {
            records: "categorias"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-producto").dynatable({
        params: {
            records: "productos"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-producto-inv").dynatable({
        params: {
            records: "productos"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-proveedor").dynatable({
        params: {
            records: "proveedores"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-cliente").dynatable({
        params: {
            records: "clientes"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-ventas").dynatable({
        params: {
            records: "ventas"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-compras").dynatable({
        params: {
            records: "compras"
        }
    })
        .bind('dynatable:afterProcess', fixTableSelect);
    $("#tabla-stock-disp").dynatable({
        params: {
            records: "productos"
        }
    })
    //------- Manejo global ---------
    //select table
    $("table[select]>tbody>tr").click(function (evt) {
        var id = $(this).parent().parent().attr("id");
        cleanData('table', id);
        var tr = $(this);
        tr.addClass('active');
        updateButtons(id);
    })

    //fix required msg
    $("[required]").attr("oninvalid", "this.setCustomValidity('Este campo es requerido.')");

    //checkbox fix
    $("span input[type=checkbox]").click(function () {
        if ($(this).parent().hasClass("checked")) {
            $(this).parent().removeClass("checked")
            $(this).val('off');
        } else {
            $(this).parent().addClass("checked")
            $(this).val('on')
        }
    })

    //radio fix
    $("span input[type=radio]").click(function () {
        var name = $(this).attr("name");
        if ($("span input[type=radio][name=" + name + "]").parent().hasClass("checked")) {
            $("span input[type=radio][name=" + name + "]").parent().removeClass("checked");
        }
        $(this).parent().addClass("checked");

    })

    //campo fecha addClass pickadate
    $('.pickadate').pickadate({
        labelMonthNext: 'Ir al mes siguiente ',
        labelMonthPrev: 'Ir al mes anterior',
        formatSubmit: 'yyyy-mm-dd',
        format: 'yyyy-mm-dd',
        monthsFull: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
        today: 'Hoy',
        clear: 'Limpiar',
        close: 'Cerrar',
    });

    var year = sessionStorage.getItem("anno");
    var mes = sessionStorage.getItem("mes");
    var last_day = new Date(year, mes, 0).getDate();
    $('.pickadate-this-month').pickadate({
        labelMonthNext: 'Ir al mes siguiente ',
        labelMonthPrev: 'Ir al mes anterior',
        formatSubmit: 'yyyy-mm-dd',
        format: 'yyyy-mm-dd',
        monthsFull: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        weekdaysShort: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
        today: 'Hoy',
        clear: 'Limpiar',
        close: 'Cerrar',
        min: [year, mes - 1, 1],
        max: [year, mes - 1, last_day]
    });

    $('.bootstrap-select').selectpicker();

    $('.bootstrap-select-search').attr("data-live-search", true);
    $('.bootstrap-select-search').selectpicker();

    //remove validations error classs from modals
    $(".modal").on("show.bs.modal", function(){
        $(this).find(".invalid").each(function(index, th){
            $(th).removeClass("invalid");
        })
    })

    //select-periodo
    $("form#select-periodo button[type=submit]").click(function () {
        selPeriodo();
    })
    //--------------------------- Login ------------------------------
    $("form[role=login] button[type=submit]").click(function () {
        var usuario = $("form[role=login] input[name=username]").val();
        sessionStorage.setItem("usuario", usuario)
    })

    $("li[logout]").click(function () {
        sessionStorage.removeItem("empresa");
        sessionStorage.removeItem("mes_mostrar");
    })

    //-------------------- Empresa ------------------------------------
    $("li a[action=add-empresa]").click(function () {
        addEmpresa();
    })

    $("li a[action=mod-empresa]").click(function () {
        modEmpresa();
    })

    $('li a[action=del-empresa]').click(function () {
        delEmpresa();
    });

    $('li a[action=sel-empresa]').click(function () {
        selEmpresa();
    });

    $('#tabla-empresa>tbody>tr').dblclick(function () {
        selEmpresa();
    });



    //------------------- Categoria   -------------------
    $("li a[action=add-categoria]").click(function () {
        addCategoria();
    })

    $("li a[action=mod-categoria]").click(function () {
        modCategoria();
    })

    $('li a[action=del-categoria]').on('click', function () {
        delCategoria();
    });

    //--------------------------- Producto ----------------------------------------
    $("li a[action=add-producto]").click(function () {
        addProducto();
    })

    $("li a[action=mod-producto]").click(function () {
        modProducto();
    })

    $('li a[action=del-producto]').on('click', function () {
        delProducto();
    });

    $("#id_unidad>option").click(function () {
        var abrv = $(this).attr("abrv");
        $("#id_abreviatura").val(abrv);
    })

    //----------------------------- Inventario ---------------------------
    $("#tabla-producto-inv>tbody>tr").click(function () {
        updateRecords("tabla-producto-inv");
    });

    //----------------------- Proveedor --------------------------------------
     $("li a[action=add-proveedor]").click(function () {
        addProveedor();
    })

    $("li a[action=mod-proveedor]").click(function () {
        modProveedor();
    })

    $('li a[action=del-proveedor]').on('click', function () {
        delProveedor();
    })
    
    
    $("button[table=tabla-proveedor][accion=add]").click(function () {
        cleanData("form", "tabla-proveedor");
        $("#form-empresa-label").html("Adicionar proveedor");
    })
    $("button[table=tabla-proveedor][accion=mod]").click(function () {
        if (!$(this).hasClass("disabled")) {
            updateRecords("tabla-proveedor");
            $("#form-empresa-label").html("Modificar proveedor");
            $("#form-proveedor").modal();
        }
    })
    $("button[table=tabla-proveedor][accion=del]").click(function () {
        if (!$(this).hasClass("disabled")) {
            var identificador = $("#tabla-proveedor tr.active td[key=no_identificacion]").html();
            $("form[accion=del] input[name=identificador]").val(identificador);
            $(".confirm-del").modal();
        }
    })

    //-------------------------------  Cliente ------------------------------
     $("li a[action=add-cliente]").click(function () {
         console.log("dfgfdgdf")
        addCliente();
    })

    $("li a[action=mod-cliente]").click(function () {
        modCliente();
    })

    $('li a[action=del-cliente]').on('click', function () {
        delCliente();
    });

    //---------------- Salida de mercancia -------------------------

    $("#datos-producto-salida [name=codigo]>option," +
        "#datos-producto-salida [name=producto]>option").click(function () {
        var id = $(this).attr("value");
        var selector_id = "#datos-producto-salida";
        llenarDatosProducto(id, selector_id);
    })

    $("#datos-producto-salida input[name=cantidad], " +
        "#importes-unitarios-salida input[name=valor-unitario]").keypress(function (e) {
        if (e.which == 13)
            llenarDatosImportesVenta()
    })

    $("#add-detalle-venta").click(function () {
        addDetalleVenta()
    })

    $("#add-salida-merc").click(function () {
        addSalidaMercancia();
    })

    $("#datos-comprobante-salida [name=identificador]>option").click(function () {
        var value = $(this).val();
        $("#datos-comprobante-salida [name=nombre]").val(value);
    })

    $("#datos-comprobante-salida [name=nombre]>option").click(function () {
        var value = $(this).val();
        $("#datos-comprobante-salida [name=identificador]").val(value);
    })

    $("#del-detalle-venta").click(function () {
        $(this).addClass("disabled");
        eliminarDetalleVenta()
    })

    //ver detalle de venta
    $("#ver-detalle-venta").click(function () {
        verDetallesVenta();
    })

    //------------- Entrada de mercancia ---------------------
    $("#datos-producto-entrada select[name=codigo]>option," +
        "#datos-producto-entrada select[name=producto]>option").click(function () {
        var id = $(this).attr("value");
        var selector_id = "#datos-producto-entrada";
        llenarDatosProducto(id, selector_id);
    })

    $("#datos-producto-entrada input[name=cantidad], " +
        "#importes-unitarios-entrada input[name=valor-unitario]").keypress(function (e) {
        //console.log(e.which)
        if (e.which == 13)
            llenarDatosImportesCompra()
    })

    $("#add-detalle-compra").click(function () {
        addDetalleCompra()
    })

    $("#add-entrada-merc").click(function () {
        addEntradaMercancia();
    })

    $("#datos-comprobante-entrada [name=identificador]>option").click(function () {
        var value = $(this).val();
        $("#datos-comprobante-entrada [name=nombre]").val(value);
    })

    $("#datos-comprobante-entrada [name=nombre]>option").click(function () {
        var value = $(this).val();
        $("#datos-comprobante-entrada [name=identificador]").val(value);
    })

    //ver detalle de compra
    $("#ver-detalle-compra").click(function () {
        verDetallesCompra();
    })

    $("#del-detalle-compra").click(function () {
        $(this).addClass("disabled");
        eliminarDetalleCompra()
    })

    //------------------------ Stock disponible ----------------------------
    $("#navtb-stock-disp button[accion=export_excel]").click(function () {
        exportarExcel();
    })
    $("#navtb-stock-disp button[accion=pdf]").click(function () {
        exportarPDF();
    })

})