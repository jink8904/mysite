from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required
import json


def list_p(producto_list):
    for i in producto_list:
        i["categoria"] = models.Categoria.objects.get(id=i.get("categoria_id"))
        i["tipo"] = models.TipoProducto.objects.get(id=i.get("tipo_id"))
        i["unidad"] = models.UnidadProducto.objects.get(id=i.get("unidad_id"))
    return producto_list


@login_required(login_url='/ingresar')
def producto(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    poductos = emp.producto_set.values()

    unidad_list = models.UnidadProducto.objects.values()
    tipo_list = models.TipoProducto.objects.values()
    cat_list = emp.categoria_set.values()

    args = {}

    datos = request.POST
    if datos:
        tipo_p = models.TipoProducto.objects.get(id=datos.get("tipo"))
        unidad_p = models.UnidadProducto.objects.get(id=datos.get("unidad"))
        categoria_p = models.Categoria.objects.get(id=datos.get("categoria"))
        if datos.get("id"):
            p = models.Producto(
                id=datos.get("id"),
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                nombre_reducido=datos.get("nombre_reducido"),
                tipo=tipo_p,
                unidad=unidad_p,
                categoria=categoria_p,
                empresa=emp
            )
            p.save()
            args['action'] = 'mod'
        else:
            p = models.Producto(
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                nombre_reducido=datos.get("nombre_reducido"),
                tipo=tipo_p,
                unidad=unidad_p,
                categoria=categoria_p,
                empresa=emp
            )
            p.save()
            inv = models.Inventario(
                costo_unitario=0,
                cantidad=0,
                producto_id=p.id,
                empresa_id=id_empresa
            )
            inv.save()
            args['action'] = 'add'

    if request.session.has_key("producto-del") == 1:
        if request.session["producto-del"]:
            args['action'] = 'del'
            request.session["producto-del"] = False

    producto_list = list_p(poductos)

    args.update(csrf(request))
    args['producto_list'] = producto_list
    args['unidad_list'] = unidad_list
    args['tipo_list'] = tipo_list
    args['cat_list'] = cat_list
    render_to_response('productos/form-producto.html', args)
    return render_to_response('productos/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_producto(request):
    producto = models.Producto.objects.get(id=request.POST.get("id"))
    producto.delete()
    request.session['producto-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")