/**
 * Created by Julio on 14-Mar-16.
 */
function submitForm(selector, fn) {
    $(selector).submit(function (evt) {
        console.log(isValid());
        if (isValid())
            fn()
        else {
            evt.preventDefault();
        }
    })

    var isValid = function () {
        var valid = true;
        $(selector + " input").each(function (index, th) {
            //validate required
            if ($(th).attr("required")) {
                var aux = checkRequired(th);
                valid = (valid) ? aux : valid;
            }
            //    validate numberfield
            if ($(th).attr("numberfield") && valid) {
                var aux = checkNumberField(th);
                valid = (valid) ? aux : valid;
            }
        })
        return valid;
    }

    var showErrors = function (th, msg) {
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
            return showErrors(th, "El campo es requerido");
        }
        return true;
    }


    var checkNumberField = function (th) {
        var regex = /^\d+$/;
        if (!regex.test($(th).val())) {
            return showErrors(th, "Solo numeros");
        }
        return true;
    }
}

