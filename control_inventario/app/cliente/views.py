from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required

def list_cliente(cliente_list):
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
    return render_to_response('clientes/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_cliente(request):
    producto = models.Cliente.objects.get(identificador=request.POST.get("identificador"))
    producto.delete();
    return HttpResponseRedirect('/cliente')
