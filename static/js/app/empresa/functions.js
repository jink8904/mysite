/**
 * Created by Julio on 09-Mar-16.
 */
function keyDownEvt(e) {
    var keyCode = e.which;
    //console.log(e.which);
    if (keyCode == 46)
        delEmpresa();
    if (keyCode == 65 && e.ctrlKey) {
        e.preventDefault();
        addEmpresa();
    }
    if (keyCode == 77 && e.ctrlKey) {
        e.preventDefault();
        modEmpresa();
    }
    if (keyCode == 83 && e.ctrlKey) {
        e.preventDefault();
        selEmpresa();
    }
}


function delEmpresa() {
    if (!$('li a[action=del-empresa]').parent().hasClass("disabled")) {
        title = "Eliminar empresa";
        text = "Est&aacute; seguro que quiere eliminar la empresa seleccionada.";
        notificacion(title, text, {
            ok: function () {
                loadMask({
                    msg: "Eliminando empresa.."
                })

                var id = $("#tabla-empresa>tbody>tr.active>td[key=id]").html();
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
                        $(location).attr("href", "/empresa");
                    }
                })
            }
        })
    }
}

function addEmpresa() {
    cleanData("form", "tabla-empresa");
    panel_title = "Adicionar empresa";
    load_msg = "Adicionando empresa...";

    $("#form-empresa-label").html(panel_title);
    $("#form-empresa").modal().on('shown.bs.modal', function () {
        $("#form-empresa input[name=ruc]").focus();
    });

    submitForm("#form-empresa form", function () {
        $("#form-empresa").hide();
        loadMask({
            msg: load_msg
        })
    });
}


function modEmpresa() {
    if (!$('li a[action=mod-empresa]').parent().hasClass("disabled")) {
        cleanData("form", "tabla-empresa");
        updateRecords("tabla-empresa");
        panel_title = "Modificar empresa";
        load_msg = "Modificando empresa...";

        $("#form-empresa-label").html(panel_title);
        $("#form-empresa").modal().on('shown.bs.modal', function () {
            $("#form-empresa input[name=codigo]").focus();
        });

        submitForm("#form-empresa form", function () {
            $("#form-empresa").hide();
            loadMask({
                msg: load_msg
            })
        });
    }
}

function selEmpresa() {
    var aux = function (result, inputOptions) {
        if (result == "")
            selPeriodo(aux)
        else {
            var mes_mostrar = "";
            for (var i in inputOptions) {
                if (inputOptions[i].value == result)
                    mes_mostrar = inputOptions[i].text
            }
            selEmpresaAux(result, mes_mostrar)
        }
    }
    selPeriodo(aux)
}

function selPeriodo(fn) {
    var inputOptions = [
        {value: "", text: "Seleccionar mes"},
        {value: "1", text: "Enero"},
        {value: "2", text: "Febrero"},
        {value: "3", text: "Marzo"},
        {value: "4", text: "Abril"},
        {value: "5", text: "Mayo"},
        {value: "6", text: "Junio"},
        {value: "7", text: "Julio"},
        {value: "8", text: "Agosto"},
        {value: "9", text: "Septiembre"},
        {value: "10", text: "Octubre"},
        {value: "11", text: "Noviembre"},
        {value: "12", text: "Diciembre"}
    ]
    if (!$('li a[action=sel-empresa]').parent().hasClass("disabled")) {
        bootbox.prompt({
            title: "Periodo",
            size: 'small',
            message: "Your message here…",
            inputType: "select",
            inputOptions: inputOptions,
            callback: function (result) {
                if (result !== null)
                    fn(result, inputOptions)
            }
        })
        $('.bootbox-input-select').selectpicker();
    }

}

function selEmpresaAux(mes, mes_mostrar) {
    empresa_seleccionada = getRecord("tabla-empresa");
    sessionStorage.setItem("empresa", JSON.stringify(empresa_seleccionada));
    sessionStorage.setItem("anno", empresa_seleccionada.anno_inicio);
    sessionStorage.setItem("mes", mes);
    sessionStorage.setItem("mes_mostrar", mes_mostrar);

    token = $("input[name=csrfmiddlewaretoken]").attr("value");
    $.ajax({
        url: "../select-empresa",
        method: "post",
        dataType: 'json',
        async: true,
        data: {
            csrfmiddlewaretoken: token,
            empresa: empresa_seleccionada,
            mes: mes
        },
        success: function (data) {
            $(location).attr("href", "../");
        }
    })

}