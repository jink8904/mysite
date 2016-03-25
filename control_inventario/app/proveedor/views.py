from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required
import json


def list_proveedor(proveedor_list):
    for ciente in proveedor_list:
        ciente["tipo_id"] = models.TipoId.objects.get(id=ciente.get("tipo_id_id"))
    return proveedor_list


@login_required(login_url='/ingresar')
def proveedor(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    c = emp.proveedor_set.values()

    tipoid_list = models.TipoId.objects.values()

    args = {}
    datos = request.POST
    if datos:
        tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
        if datos.get("id"):
            p = models.Proveedor(
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
            p = models.Proveedor(
                identificador=datos.get("identificador"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                tipo_id=tipo_id,
                empresa=emp
            )
            p.save()
            args['action'] = 'add'

    if request.session.has_key("proveedor-del") == 1:
        if request.session["proveedor-del"]:
            args['action'] = 'del'
            request.session["proveedor-del"] = False

    proveedor_list = list_proveedor(c)
    args.update(csrf(request))
    args['proveedor_list'] = proveedor_list
    args['tipoid_list'] = tipoid_list
    render_to_response('proveedores/form-proveedor.html', args)
    return render_to_response('proveedores/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_proveedor(request):
    proveedor = models.Proveedor.objects.get(id=request.POST.get("id"))
    proveedor.delete()
    request.session['proveedor-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
