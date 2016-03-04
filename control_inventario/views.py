from builtins import print
from datetime import timedelta
from xml.sax.saxutils import prepare_input_source
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.core.serializers.json import DjangoJSONEncoder
from control_inventario import forms
from control_inventario import models
# from XlsxWriter import xlsxwriter
import json
# users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# def export(request):
#     workbook = xlsxwriter.Workbook('exports/hello.xlsx')
#     worksheet = workbook.add_worksheet()
#
#     worksheet.write('A1', 'Hello world')
#
#     workbook.close()


# Login
def ingresar(request):
    args = {}
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    request.session["user"] = usuario
                    return HttpResponseRedirect('/empresa')
                else:
                    args['error'] = "El usuario no se encuetra activo."
            else:
                args['error'] = "Error en la autenticacion."
    return render_to_response("login/login-form.html", args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar_session(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/ingresar')
def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))


# --------- Empresa ------------
@login_required(login_url='/ingresar')
def empresa(request):
    empresa_list = models.Empresa.objects.values()
    datos = request.POST
    if datos:
        if datos.get("id"):
            for obj in empresa_list:
                id = obj.get("id")
                if str(id) == datos.get("id"):
                    emp = models.Empresa(
                        id=id,
                        nombre=datos.get("nombre"),
                        anno_inicio=datos.get("anno_inicio"),
                        ruc=datos.get("ruc"),
                        direccion=datos.get("direccion"),
                    )
                    emp.save()
        else:
            form = forms.EmpresaForm(request.POST)
            if form.is_valid():
                form.save()
        return HttpResponseRedirect('/empresa', {"empresa_list": empresa_list})
    else:
        form = forms.EmpresaForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['empresa_list'] = empresa_list
    return render_to_response('empresa/empresa.html', args)


def select_empresa(request):
    datos = request.POST
    request.session['empresa'] = {
        "ruc": datos.get("empresa[ruc]"),
        "nombre": datos.get("empresa[nombre]"),
        "id": datos.get("empresa[id]"),
        "direccion": datos.get("empresa[direccion]"),
        "anno_inicio": datos.get("empresa[anno_inicio]"),
        "mes": datos.get("empresa[mes]"),
    }
    json_data = json.dumps({"success": True})
    return HttpResponse(json_data, mimetype="application/json")


@login_required(login_url='/ingresar')
def del_empresa(request):
    empresa = models.Empresa.objects.get(ruc=request.POST.get("ruc"))
    empresa.delete();
    return HttpResponseRedirect('/empresa')


# --------- Categoria ----------
@login_required(login_url='/ingresar')
def categoria(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    categoria_list = emp.categoria_set.values()
    datos = request.POST
    if datos:
        if datos.get("id"):
            for obj in categoria_list:
                id = obj.get("id")
                if str(id) == datos.get("id"):
                    cat = models.Categoria(
                        id=id,
                        codigo=datos.get("codigo"),
                        denominacion=datos.get("denominacion")
                    )
                    cat.save()
                    # cat.empresa.add(empresa_p);
        else:
            cat = models.Categoria(
                codigo=datos.get("codigo"),
                denominacion=datos.get("denominacion")
            )
            cat.save()
            cat.empresa.add(emp)
        return HttpResponseRedirect('/categorias', {"categoria_list": categoria_list})
    else:
        form = forms.CategoriaForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['categoria_list'] = categoria_list

    return render_to_response('categoria/categoria.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_categoria(request):
    categoria = models.Categoria.objects.get(codigo=request.POST.get("codigo"))
    categoria.delete();
    return HttpResponseRedirect('/categorias')


# ---- Producto  -------
def list_p(producto_list):
    for i in producto_list:
        i["categoria"] = models.Categoria.objects.get(id=i.get("categoria_id"))
        i["tipo"] = models.TipoProducto.objects.get(id=i.get("tipo_id"))
        i["unidad"] = models.UnidadProducto.objects.get(id=i.get("unidad_id"))
    return producto_list;


@login_required(login_url='/ingresar')
def producto(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    p = emp.producto_set.values()
    producto_list = list_p(p)
    unidad_list = models.UnidadProducto.objects.values()
    tipo_list = models.TipoProducto.objects.values()
    cat_list = emp.categoria_set.values()
    datos = request.POST
    if datos:
        if datos.get("id"):
            for obj in producto_list:
                id = obj.get("id")
                if str(id) == datos.get("id"):
                    form = forms.ProductoForm(datos)
                    tipo_p = models.TipoProducto.objects.get(id=datos.get("tipo"))
                    unidad_p = models.UnidadProducto.objects.get(id=datos.get("unidad"))
                    categoria_p = models.Categoria.objects.get(id=datos.get("categoria"))
                    p = models.Producto(
                        id=id,
                        codigo=datos.get("codigo"),
                        nombre=datos.get("nombre"),
                        nombre_reducido=datos.get("nombre_reducido"),
                        tipo=tipo_p,
                        unidad=unidad_p,
                        categoria=categoria_p,
                    )
                    p.save()
                    break
        else:
            form = forms.ProductoForm(datos)
            tipo_p = models.TipoProducto.objects.get(id=datos.get("tipo"))
            unidad_p = models.UnidadProducto.objects.get(id=datos.get("unidad"))
            categoria_p = models.Categoria.objects.get(id=datos.get("categoria"))
            p = models.Producto(
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                nombre_reducido=datos.get("nombre_reducido"),
                tipo=tipo_p,
                unidad=unidad_p,
                categoria=categoria_p
            )
            p.save()
            p.empresa.add(emp)
            inv = models.Inventario(
                costo_unitario=0,
                cantidad=0,
                producto_id=p.id,
                empresa_id=id_empresa
            )
            inv.save()
        return HttpResponseRedirect('/productos', {"producto_list": producto_list})
    else:
        form = forms.ProductoForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['producto_list'] = producto_list
    args['unidad_list'] = unidad_list
    args['tipo_list'] = tipo_list
    args['cat_list'] = cat_list
    render_to_response('productos/form-producto.html', args)
    return render_to_response('productos/productos.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_producto(request):
    producto = models.Producto.objects.get(codigo=request.POST.get("codigo"))
    producto.delete();
    return HttpResponseRedirect('/productos')


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

    return render_to_response('inventario_inicial/inventario_inicial.html', args,
                              context_instance=RequestContext(request))


# ----------- Proveedor -----------
def list_proveedor(proveedor_list):
    # proveedor_list = models.Proveedor.objects.values()
    for i in proveedor_list:
        i["tipo_id"] = models.TipoId.objects.get(id=i.get("tipo_id_id"))
    return proveedor_list;


@login_required(login_url='/ingresar')
def proveedor(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    p = emp.proveedor_set.values()

    proveedor_list = list_proveedor(p)
    tipoid_list = models.TipoId.objects.values()
    datos = request.POST
    if datos:
        if datos.get("id"):
            for obj in proveedor_list:
                id = obj.get("id")
                if str(id) == datos.get("id"):
                    tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
                    p = models.Proveedor(
                        id=id,
                        identificador=datos.get("identificador"),
                        nombre=datos.get("nombre"),
                        direccion=datos.get("direccion"),
                        tipo_id=tipo_id,
                    )
                    p.save()
                    break
        else:
            form = forms.ProductoForm(datos)
            tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
            p = models.Proveedor(
                identificador=datos.get("identificador"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                tipo_id=tipo_id,
            )
            p.save()
            p.empresa.add(emp);
        return HttpResponseRedirect('/proveedor', {"proveedor_list": proveedor_list})
    else:
        form = forms.ProductoForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['proveedor_list'] = proveedor_list
    args['tipoid_list'] = tipoid_list
    render_to_response('proveedores/form-proveedor.html', args)
    return render_to_response('proveedores/proveedor.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_proveedor(request):
    producto = models.Proveedor.objects.get(identificador=request.POST.get("identificador"))
    producto.delete();
    return HttpResponseRedirect('/proveedor')


# --------------- Cliente ----------------
def list_cliente(cliente_list):
    # cliente_list = models.Cliente.objects.values()
    for i in cliente_list:
        i["tipo_id"] = models.TipoId.objects.get(id=i.get("tipo_id_id"))
    return cliente_list;


@login_required(login_url='/ingresar')
def cliente(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    c = emp.cliente_set.values()

    cliente_list = list_cliente(c)
    tipoid_list = models.TipoId.objects.values()
    datos = request.POST
    if datos:
        if datos.get("id"):
            for obj in cliente_list:
                id = obj.get("id")
                if str(id) == datos.get("id"):
                    tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
                    p = models.Cliente(
                        id=id,
                        identificador=datos.get("identificador"),
                        nombre=datos.get("nombre"),
                        direccion=datos.get("direccion"),
                        tipo_id=tipo_id,
                    )
                    p.save()
                    break
        else:
            form = forms.ProductoForm(datos)
            tipo_id = models.TipoId.objects.get(id=datos.get("tipo_id"))
            p = models.Cliente(
                identificador=datos.get("identificador"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                tipo_id=tipo_id,
            )
            p.save()
            p.empresa.add(emp);
        return HttpResponseRedirect('/cliente', {"cliente_list": cliente_list})
    else:
        form = forms.ProductoForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['cliente_list'] = cliente_list
    args['tipoid_list'] = tipoid_list
    render_to_response('clientes/form-cliente.html', args)
    return render_to_response('clientes/cliente.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_cliente(request):
    producto = models.Cliente.objects.get(identificador=request.POST.get("identificador"))
    producto.delete();
    return HttpResponseRedirect('/cliente')


# ----------- Salida de mercancia ------------------
def update_prod_list(emp):
    producto_list = emp.producto_set.values()
    inventario_list = emp.inventario_set.values()
    for prod in producto_list:
        id = prod.get("id")
        inv = inventario_list.get(producto=id)
        prod["stock"] = inv["cantidad"]
    return producto_list


def update_venta_list(emp):
    venta_list = emp.venta_set.values()
    for i in venta_list:
        i['tipo_comprobante'] = models.TipoComprobante.objects.get(id=i["tipo_comprobante_id"]).denominacion
        i['cliente'] = models.Cliente.objects.get(id=i["cliente_id"]).nombre
    return venta_list


def salida_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    comprobante_list = models.TipoComprobante.objects.values()
    cliente_list = emp.cliente_set.values()
    producto_list = update_prod_list(emp)
    venta_list = update_venta_list(emp)
    tipo_operacion_list = models.TipoOperacion.objects.values()

    args = {}
    args["comprobante_list"] = comprobante_list
    args["cliente_list"] = cliente_list
    args["producto_list"] = producto_list
    args["venta_list"] = venta_list
    args["tipo_operacion_list"] = tipo_operacion_list
    return render_to_response('salida_mercancia/salida_mercancia.html', args, context_instance=RequestContext(request))


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
            igv = igv + float(detalle['igv_total'])
            subtotal = subtotal + float(detalle['valor_venta'])
            total = total + float(detalle['precio_venta'])
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


# ----------- Entrada de mercancia ------------------
def update_prod_list(emp):
    producto_list = emp.producto_set.values()
    inventario_list = emp.inventario_set.values()
    for prod in producto_list:
        id = prod.get("id")
        inv = inventario_list.get(producto=id)
        prod["stock"] = inv["cantidad"]
    return producto_list


def update_compra_list(emp):
    compra_list = emp.compra_set.values()
    for i in compra_list:
        i['tipo_comprobante'] = models.TipoComprobante.objects.get(id=i["tipo_comprobante_id"]).denominacion
        i['proveedor'] = models.Proveedor.objects.get(id=i["proveedor_id"]).nombre
    return compra_list


def entrada_mercancia(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    comprobante_list = models.TipoComprobante.objects.values()
    proveedor_list = emp.proveedor_set.values()
    producto_list = update_prod_list(emp)
    compra_list = update_compra_list(emp)
    tipo_operacion_list = models.TipoOperacion.objects.values()

    args = {}
    args["comprobante_list"] = comprobante_list
    args["proveedor_list"] = proveedor_list
    args["producto_list"] = producto_list
    args["compra_list"] = compra_list
    args["tipo_operacion_list"] = tipo_operacion_list

    return render_to_response('entrada_mercancia/entrada_mercancia.html', args,
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


# ------------ Registro de ventas -----------------
def registro_ventas(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    estadoPLE_list = models.EstadoPLE.objects.values()
    comprobante_list = models.TipoComprobante.objects.values()
    cliente_list = emp.cliente_set.values()

    args = {}
    args['estadoPLE_list'] = estadoPLE_list
    args['cliente_list'] = cliente_list
    args['comprobante_list'] = comprobante_list
    return render_to_response('registro_ventas/registro_ventas.html', args, context_instance=RequestContext(request))
