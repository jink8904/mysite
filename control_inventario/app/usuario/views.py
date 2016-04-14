from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


def list_usuario(usuario_list):
    for ciente in usuario_list:
        ciente["tipo_id"] = models.TipoId.objects.get(id=ciente.get("tipo_id_id"))
    return usuario_list


@login_required(login_url='/ingresar')
def usuario(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    args = {}
    datos = request.POST
    if datos:
        if datos.get("activo"):
            datos["activo"] = True
        else:
            datos["activo"] = False
        if datos.get("id"):
            user = User(
                id=datos.get("id"),
                username=datos.get("usuario"),
                first_name=datos.get("nombre"),
                last_name=datos.get("apellidos"),
                email=datos.get("correo"),
                is_active=datos.get("activo")
            )
            user.save()
            args['action'] = 'mod'
        else:
            if (User.objects.filter(username=datos.get("usuario")).__len__() > 0):
                args['action'] = 'exist'
            else:
                user = User.objects.create_user(
                    username=datos.get("usuario"),
                    password=datos.get("usuario"),
                    first_name=datos.get("nombre"),
                    last_name=datos.get("apellidos"),
                    email=datos.get("correo")
                )
                user.is_active = datos.get("activo")
                user.save()
                args['action'] = 'add'

    if request.session.has_key("usuario-del") == 1:
        if request.session["usuario-del"]:
            args['action'] = 'del'
            request.session["usuario-del"] = False

    usuario_list = User.objects.values()
    args.update(csrf(request))
    args['usuario_list'] = usuario_list
    return render_to_response('usuario/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_usuario(request):
    usuario = User.objects.get(id=request.POST.get("id"))
    usuario.delete()
    request.session['usuario-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
