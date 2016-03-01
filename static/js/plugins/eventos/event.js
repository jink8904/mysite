/*!
 * Events v1.1
 * VideoVigilancia - XETID
 * (c) 2014 Danny Almeida Perez
 */
/*
 * Requiere event.css para los estilos de los eventos.
 * Requiere jQuery v1.9 o mayor.
 * Solamente esta probado en ExtJS 2.2 (otras versiones sin testear)
 */

Eventos = function () {


    this.containerTop = $('<div/>', {
        'class': 'evt-container-top',
    });

    this.containerRigth = $('<div/>', {
        'class': 'evt-container-rigth',
    });

    var body = $('body');
    this.containerTop.appendTo(body);
    this.containerRigth.appendTo(body);

    var _this = this;

    this.Mensaje = function (message, options) {


        var defaults = {
            /* Duracion del mensaje en el area */
            duration: 3, // segundos

            position: 'top', // [top , right]

            /* Tipo de Mensaje (carga todo los css correspondientes del tipo de mensaje)*/
            type: 'information', // [information, success, warning , error, alarma,confirm(no implementado todavia)]

            /* Si  presenta color de fondo el mensaje*/
            frame: true, // [true, false]

            /* Bordes animados del mensaje*/
            borderAnimate: false, // [true, false] (no implementado todavia)

            /* Si presenta sombra el mensaje */
            shadow: true, // [true, false]

            /* Si va a tener animacion el mensaje cuadno se muestre y cuadno se oculte */
            animate: true, // [true, false]

            /* Tipo de animacion del mensaje */
            animation: 'fade', // [fade, bounce, slide, scale]

        };

        var settings = $.extend({}, defaults, options);

        var mensaje = {
            'top': function () {

                $('.evt-top').remove();
                var mensajee = $('<div/>', {
                    'class': 'evt-top',
                });

                var borderRad = $('<div/>', {
                    'class': 'borRad ' + 'msg-' + settings.type
                });
                var borderCirc = $('<div/>', {
                    'class': 'borCirc ' + 'msg-' + settings.type
                });
                var icon = $('<div/>', {
                    'class': 'image ' + 'img-' + settings.type
                });

                if (settings.shadow) {
                    borderRad.addClass('shadow-' + settings.type);
                    borderCirc.addClass('shadow-' + settings.type);
                }

                if (settings.frame) {
                    borderRad.addClass('bg-' + settings.type);
                    borderCirc.addClass('bg-' + settings.type);
                    icon.addClass('bg-' + settings.type);
                }

                var title = "";

                var type = {
                    'information': function () {
                        title = "Información";
                    },
                    'success': function () {
                        title = "Información";
                    },
                    'error': function () {
                        title = "Error";
                    },
                    'warning': function () {
                        title = "Advertencia";
                    },
                    'confirm': function () {
                        title = "Confirmación";
                    },
                    'default': function () {
                        console.error('Tipo de mensaje no valido');
                        exit;
                    },
                };

                if (type[settings.type]) {
                    type[settings.type]();
                } else {
                    type['default']();
                }

                var pTitle = $('<p/>', {
                    'class': 'title ' + 'title-' + settings.type,
                    html: title,
                });

                var pMessage = $('<p/>', {
                    'class': 'message',
                    html: message,
                });

                var btnsMessage = $('<div/>', {
                    'class': 'btns',
                    html: '<button type="button" class="btn btn-primary btn-xs" id="aceptar"> Aceptar\n\
                             <button type="button" class="btn btn-danger btn-xs" id="cancelar">Cancelar',
                });

                mensajee.appendTo(_this.containerTop);
                borderRad.appendTo(mensajee);
                pTitle.appendTo(borderRad);
                pMessage.appendTo(borderRad);
                if (settings.type == 'confirm') {
                    btnsMessage.appendTo(borderRad);
                    settings.duration = 60;
                    $('#aceptar').click(function () {
                        settings.callback(settings.params);
                    });
                }

                borderCirc.appendTo(mensajee);
                icon.appendTo(mensajee);

                var cerrarMensaje = function () {

                    if (settings.animate) {
                        mensajee.removeClass();
                        mensajee.addClass(settings.animation + 'OutUp');
                        mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                            mensajee.remove();
                        });
                    } else
                        mensajee.remove();
                };

                if (settings.animate) {
                    mensajee.addClass(settings.animation + 'InUp');

                    mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                        mensajee.removeClass(settings.animation + 'InUp');

                        setTimeout(function () {
                            mensajee.addClass(settings.animation + 'OutUp');
                            mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                                mensajee.remove();
                            });
                        }, settings.duration * 1000);
                    });

                    icon.click(cerrarMensaje);
                    borderCirc.click(cerrarMensaje);
                    borderRad.click(cerrarMensaje);
                } else {
                    setTimeout(function () {
                        mensajee.remove();
                    }, settings.duration * 1000)
                    icon.click(cerrarMensaje);
                    borderCirc.click(cerrarMensaje);
                    borderRad.click(cerrarMensaje);
                }
            },
            'right': function () {

                var mensajee = $('<div/>', {
                    'class': 'evt-rigth',
                });

                var borderRad = $('<div/>', {
                    'class': 'borRad-rigth ' + 'msg-' + settings.type
                });

                var icon = $('<div/>', {
                    'class': 'image-rigth ' + 'img-' + settings.type,
                    html: '&nbsp;'
                });


                var contMessage = $('<div/>', {
                    'class': 'cont-message',
                });

                var pMessage = $('<p/>', {
                    'class': 'message',
                    html: message,
                })

                if (settings.shadow) {
                    borderRad.addClass('shadow-' + settings.type);
                    // borderCirc.addClass('shadow-' + settings.type);
                }
                if (settings.frame) {
                    borderRad.addClass('bg-' + settings.type);
                    icon.addClass('bg-' + settings.type);
                }


                mensajee.appendTo(_this.containerRigth);
                borderRad.appendTo(mensajee);
                icon.appendTo(borderRad);
                contMessage.appendTo(borderRad);

                pMessage.appendTo(contMessage);

                var cerrarMensaje = function () {

                    if (settings.animate) {
                        // mensajee.removeClass(settings.animation + 'InRight');
                        mensajee.addClass(settings.animation + 'OutRight');
                        mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                            mensajee.remove();
                        })
                    } else
                        mensajee.remove();

                }

                if (settings.animate) {

                    mensajee.addClass(settings.animation + 'InRight');

                    mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                        mensajee.removeClass(settings.animation + 'InRight');

                        setTimeout(function () {
                            mensajee.addClass(settings.animation + 'OutRight');
                            mensajee.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
                                mensajee.remove();
                            })
                        }, settings.duration * 1000)
                    })

                    icon.click(cerrarMensaje);
                    contMessage.click(cerrarMensaje);
                    borderRad.click(cerrarMensaje);


                } else {

                    setTimeout(function () {
                        mensajee.remove();
                    }, settings.duration * 1000)

                    icon.click(cerrarMensaje);
                    contMessage.click(cerrarMensaje);
                    borderRad.click(cerrarMensaje);
                }

            },
            'default': function () {
                console.error('mensaje no valido');
                exit;
            },
        };

        if (mensaje[settings.position]) {
            mensaje[settings.position]();
        } else {
            mensaje['default']();
        }
    }
}
