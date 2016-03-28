/**
 * Created by Julio on 14-Mar-16.
 */
function submitForm(selector, fn) {
    $(selector).submit(function (evt) {
        if (isValid())
            fn()
        else {
            evt.preventDefault();
        }
    })

    var isValid = function () {
        var valid = true;
        //select form inputs
        $(selector + " input").each(function (index, th) {
            //validate required
            if ($(th).attr("required")) {
                var aux = checkRequired(th);
                valid = (valid) ? aux : valid;
            }
            //    validate numberfield
            if ($(th).attr("numberfield") != undefined && valid) {
                var aux = checkNumberField(th);
                valid = (valid) ? aux : valid;
            }
            //    validate validator
            if ($(th).attr("validator") && valid) {
                var aux = checkValidator(th);
                valid = (valid) ? aux : valid;
            }
        })
        //select form selects
        $(selector + " select").each(function (index, th) {
            if ($(th).attr("required")) {
                if ($(th).val() == "") {
                    $(th).next().children(":first").addClass("invalid");
                    valid = false;
                    $(th).change(function () {
                        //var selected = $(this).find("option:selected").val();
                        if ($(th).next().children(":first").hasClass("invalid")) {
                            $(th).next().children(":first").removeClass("invalid")
                        }
                    })
                }
            }
        })
        return valid;
    }

    var showErrorTooltip = function (th, msg) {
        if ($(th).hasClass("tooltipstered"))
            $(th).tooltipster("destroy");
        $(th).tooltipster({
            content: msg,
            position: "bottom",
            theme: "tooltipster-error",
        });
        $(th).addClass("invalid");
        $(th).focusin(function () {
            $(th).removeClass("invalid");
            $(th).tooltipster("disable");
        })
        return false;
    }

    var checkRequired = function (th) {
        if ($(th).val() == "") {
            return showErrorTooltip(th, "El campo es requerido");
        }
        return true;
    }


    var checkNumberField = function (th) {
        var regex = /^\d+$/;
        if (!regex.test($(th).val())) {
            return showErrorTooltip(th, "Solo numeros");
        }
        return true;
    }


    var checkValidator = function (th) {
        var validator = $(th).attr("validator");
        var regex = "";
        var msg = "";
        switch (validator) {
            case "v_11digits":
                regex = /^\d{11,11}$/
                msg = "Solo admite números enteros de 11 digitos"
                break
            default :

                break
        }
        if (!regex.test($(th).val())) {
            return showErrorTooltip(th, msg);
        }
        return true;
    }
}

