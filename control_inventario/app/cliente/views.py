from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required
import json


def list_cliente(cliente_list):
    for ciente in cliente_list:
        ciente["tipo_id"] = models.TipoId.objects.get(id=ciente.get("tipo_id_id"))
    return cliente_list


@login_required(login_url='/ingresar')
def cliente(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    c = emp.cliente_set.values()

    tipoid_list = models.TipoId.objects.values()

    args = {}
    datos = request.POST
    if datos:
        tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
        if datos.get("id"):
            p = models.Cliente(
                id=datos.get("id"),
                identificador=datos.get("identificador"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                tipo_id=tipo_id,
                empresa=emp
            )
            p.save()
            args['action'] = 'mod'
        else:
            p = models.Cliente(
                identificador=datos.get("identificador"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                tipo_id=tipo_id,
                empresa=emp
            )
            p.save()
            args['action'] = 'add'

    if request.session.has_key("cliente-del") == 1:
        if request.session["cliente-del"]:
            args['action'] = 'del'
            request.session["cliente-del"] = False

    cliente_list = list_cliente(c)
    args.update(csrf(request))
    args['cliente_list'] = cliente_list
    args['tipoid_list'] = tipoid_list
    render_to_response('clientes/form-cliente.html', args)
    return render_to_response('clientes/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_cliente(request):
    cliente = models.Cliente.objects.get(id=request.POST.get("id"))
    cliente.delete()
    request.session['cliente-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
