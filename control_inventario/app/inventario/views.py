from builtins import print
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
import json
# from XlsxWriter import xlsxwriter
# users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# ------------ Inventario ------------
def list_p_inv(producto_list):
    for i in producto_list:
        i["categoria"] = models.Categoria.objects.get(id=i.get("categoria_id"))
        i["tipo"] = models.TipoProducto.objects.get(id=i.get("tipo_id"))
        i["unidad"] = models.UnidadProducto.objects.get(id=i.get("unidad_id"))
        inv = models.Inventario.objects.get(producto=i.get("id"))
        i["cantidad"] = inv.cantidad
        i["costo_unitario"] = inv.costo_unitario
        i["costo_total"] = inv.costo_unitario * inv.cantidad
    return producto_list;


def inventario_inicial(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    p = emp.producto_set.values()
    producto_list = list_p_inv(p)

    datos = request.POST
    if datos:
        if datos.get("id"):
            inv = models.Inventario.objects.get(producto=datos.get("id"))
            inv.cantidad = datos.get("cantidad")
            inv.costo_unitario = datos.get("costo_unitario")
            inv.save()

    args = {}
    args.update(csrf(request))
    print(producto_list)
    args["productos"] = producto_list

    return render_to_response('inventario_inicial/main.html', args,
                              context_instance=RequestContext(request))
