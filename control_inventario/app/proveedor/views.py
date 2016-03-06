from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required

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
    return render_to_response('proveedores/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_proveedor(request):
    producto = models.Proveedor.objects.get(identificador=request.POST.get("identificador"))
    producto.delete();
    return HttpResponseRedirect('/proveedor')
