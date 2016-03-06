from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required


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
    return render_to_response('productos/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_producto(request):
    producto = models.Producto.objects.get(codigo=request.POST.get("codigo"))
    producto.delete();
    return HttpResponseRedirect('/productos')
