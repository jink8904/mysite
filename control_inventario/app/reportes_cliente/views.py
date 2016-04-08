from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required
import json


def list_cliente(cliente_list):
    for cliente in cliente_list:
        cliente["tipo_id"] = models.TipoId.objects.get(id=cliente.get("tipo_id_id"))
    return cliente_list


@login_required(login_url='/ingresar')
def reporte_cliente(request, tipo):
    print(tipo)
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    args = {}
    args["tipo"] = tipo

    cliente_list = emp.cliente_set.values()
    cliente_list = list_cliente(cliente_list)

    args["form"] = True
    args["cliente_list"] = cliente_list
    if (tipo == "diario"):
        sfsd = 0

    return render_to_response('reportes_cliente/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_cliente(request):
    cliente = models.Cliente.objects.get(id=request.POST.get("id"))
    cliente.delete()
    request.session['cliente-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
