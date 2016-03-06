from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
# users
from django.contrib.auth.decorators import login_required

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

    return render_to_response('categoria/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_categoria(request):
    categoria = models.Categoria.objects.get(codigo=request.POST.get("codigo"))
    categoria.delete();
    return HttpResponseRedirect('/categorias')
