from builtins import print
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from control_inventario import forms, models
import json, datetime
from django.contrib.auth.decorators import login_required

# ----------- Entrada de mercancia ------------------
def update_prod_list(emp):
    producto_list = emp.producto_set.values()
    inventario_list = emp.inventario_set.values()
    for prod in producto_list:
        id = prod.get("id")
        inv = inventario_list.get(producto=id)
        prod["stock"] = inv["cantidad"]
    return producto_list


def update_compra_list(emp, mes):
    compra_list = emp.compra_set.filter(fecha__month=mes)
    compra_list = compra_list.order_by("fecha")
    compra_list = compra_list.values()
    for i in compra_list:
        i['tipo_comprobante'] = models.TipoComprobante.objects.get(id=i["tipo_comprobante_id"]).denominacion
        i['proveedor'] = models.Proveedor.objects.get(id=i["proveedor_id"]).nombre
    return compra_list

@login_required(login_url='/ingresar')
def entrada_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    mes = request.session['mes']

    comprobante_list = models.TipoComprobante.objects.values()
    proveedor_list = emp.proveedor_set.values()
    producto_list = update_prod_list(emp)
    compra_list = update_compra_list(emp, mes)
    tipo_operacion_list = models.TipoOperacion.objects.values()

    args = {}
    args["comprobante_list"] = comprobante_list
    args["proveedor_list"] = proveedor_list
    args["producto_list"] = producto_list
    args["compra_list"] = compra_list
    args["tipo_operacion_list"] = tipo_operacion_list

    return render_to_response('entrada_mercancia/main.html', args,
                              context_instance=RequestContext(request))


def add_entrada_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    producto_list = update_prod_list(emp)

    datos = request.POST
    if datos:
        datos_compra = json.loads(datos.get("datos_compra"))
        detalle_list = json.loads(datos.get("detalle_compra_list"))
        igv = 0
        subtotal = 0
        total = 0
        for i in detalle_list:
            detalle = detalle_list[i]
            igv = igv + detalle['igv_total']
            subtotal = subtotal + detalle['valor_compra']
            total = total + detalle['precio_compra']
        proveedor = models.Proveedor.objects.get(id=datos_compra['proveedor'])
        tipo_comprobante = models.TipoComprobante.objects.get(id=datos_compra['tipo_comprobante'])
        compra = models.Compra(
            fecha=datos_compra['fecha'],
            serie=datos_compra['serie'],
            numero=datos_compra['numero'],
            subtotal=subtotal,
            igv=igv,
            total=total,
            tipo_comprobante=tipo_comprobante,
            proveedor=proveedor,
            empresa=emp
        )
        compra.save()
        for i in detalle_list:
            detalle = detalle_list[i]
            prod = models.Producto.objects.get(id=i)
            inv = models.Inventario.objects.get(producto_id=i)
            inv.cantidad = inv.cantidad + detalle['cant']
            inv.save()
            # salvar al historico
            inv_hist = models.InventarioHist(
                fecha_real=datetime.datetime.now(),
                fecha_operacion=compra.fecha,
                tipo_operacion="entrada",
                cantidad=detalle['cant'],
                cantidad_final=inv.cantidad,
                inventario=inv
            )
            inv_hist.save()
            # salvar detalle
            detalle_obj = models.DetalleCompra(
                descripcion=prod.nombre,
                cantidad=detalle['cant'],
                valor_unitario=detalle['valor_unitario'],
                valor_venta=detalle['valor_compra'],
                igv=detalle['igv_total'],
                importe=detalle['precio_compra'],
                producto=prod,
                compra=compra
            )
            detalle_obj.save()

        json_data = json.dumps({"success": True})
        return HttpResponse(json_data, mimetype="application/json")


def detalle_compra(request):
    datos = request.POST
    d_list = []
    if datos:
        id_compra = datos.get("id_compra")
        detalles_list = models.DetalleCompra.objects.filter(compra_id=id_compra).values()
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