# _*_ coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from control_inventario import models
import json, datetime

from django.contrib.auth.decorators import login_required


def update_prod_list(emp):
    producto_list = emp.producto_set.values()
    inventario_list = emp.inventario_set.values()
    for prod in producto_list:
        id = prod.get("id")
        inv = inventario_list.get(producto=id)
        prod["stock"] = inv["cantidad"]
    return producto_list


def update_venta_list(emp, mes):
    venta_list = emp.venta_set.filter(fecha__month=mes)
    venta_list = venta_list.order_by("fecha")
    venta_list = venta_list.values()
    for venta in venta_list:
        venta['tipo_comprobante'] = models.TipoComprobante.objects.get(id=venta["tipo_comprobante_id"]).denominacion
        venta['cliente'] = models.Cliente.objects.get(id=venta["cliente_id"]).nombre
    return venta_list


@login_required(login_url='/ingresar')
def salida_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    mes = request.session["mes"]
    emp = models.Empresa.objects.get(id=id_empresa)
    args = {}

    comprobante_list = models.TipoComprobante.objects.values()
    cliente_list = emp.cliente_set.values()
    producto_list = update_prod_list(emp)
    venta_list = update_venta_list(emp, mes)
    tipo_operacion_list = models.TipoOperacion.objects.values()

    if request.session.has_key("del-venta") == 1:
        if (request.session["del-venta"]):
            args["action"] = "del"
            request.session["del-venta"]=False

    args["comprobante_list"] = comprobante_list
    args["cliente_list"] = cliente_list
    args["producto_list"] = producto_list
    args["venta_list"] = venta_list
    args["tipo_operacion_list"] = tipo_operacion_list

    return render_to_response('salida_mercancia/main.html', args, context_instance=RequestContext(request))


def add_salida_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    datos = request.POST
    if datos:
        datos_venta = json.loads(datos.get("datos_venta"))
        detalle_list = json.loads(datos.get("detalle_venta_list"))
        igv = 0
        subtotal = 0
        total = 0
        for i in detalle_list:
            detalle = detalle_list[i]
            igv += float(detalle['igv_total'])
            subtotal += float(detalle['valor_venta'])
            total += float(detalle['precio_venta'])
        cliente = models.Cliente.objects.get(id=datos_venta['cliente'])
        tipo_comprobante = models.TipoComprobante.objects.get(id=datos_venta['tipo_comprobante'])
        venta = models.Venta(
            fecha=datos_venta['fecha'],
            serie=datos_venta['serie'],
            numero=datos_venta['numero'],
            subtotal=subtotal,
            igv=igv,
            total=total,
            tipo_comprobante=tipo_comprobante,
            cliente=cliente,
            empresa=emp
        )
        venta.save()
        for i in detalle_list:
            detalle = detalle_list[i]
            prod = models.Producto.objects.get(id=i)
            inv = models.Inventario.objects.get(producto_id=i)
            inv.cantidad = inv.cantidad - detalle['cant']
            inv.save()
            # salvar al historico
            inv_hist = models.InventarioHist(
                fecha_real=datetime.datetime.now(),
                fecha_operacion=venta.fecha,
                tipo_operacion="salida",
                cantidad=detalle['cant'],
                cantidad_final=inv.cantidad,
                producto=prod,
                empresa=emp
            )
            inv_hist.save()
            # salvar detalles
            detalle_obj = models.DetalleVenta(
                descripcion=prod.nombre,
                cantidad=detalle['cant'],
                valor_unitario=detalle['valor_unitario'],
                valor_venta=detalle['valor_venta'],
                igv=detalle['igv_total'],
                importe=detalle['precio_venta'],
                producto=prod,
                venta=venta
            )
            detalle_obj.save()

        json_data = json.dumps({"success": True})
        return HttpResponse(json_data, mimetype="application/json")


# @login_required(login_url='/ingresar')
# def del_venta(request):
    # venta = models.Venta.objects.get(id=request.POST.get("id"))
    # venta.delete()
    # request.session['del-venta'] = True
    #
    # args = {}
    # args['success'] = True
    # json_data = json.dumps(args)
    # return HttpResponse(json_data, mimetype="application/json")


def detalle_venta(request):
    datos = request.POST
    d_list = []
    if datos:
        id_venta = datos.get("id_venta")
        detalles_list = models.DetalleVenta.objects.filter(venta_id=id_venta).values()
        for i in detalles_list:
            i["valor_unitario"] = float(i['valor_unitario'])
            i["importe"] = float(i['importe'])
            i["igv"] = float(i['igv'])
            i["valor_venta"] = float(i['valor_venta'])
            prod = models.Producto.objects.get(id=i['producto_id'])
            i['codigo'] = prod.codigo
            d_list.append(i)

    args = {}
    args['d_list'] = d_list
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
