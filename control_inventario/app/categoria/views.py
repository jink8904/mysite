from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
import json
# users
from django.contrib.auth.decorators import login_required


# --------- Categoria ----------
@login_required(login_url='/ingresar')
def categoria(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    datos = request.POST
    args = {}
    args['categoria_list'] = emp.categoria_set.values()

    if datos:
        if datos.get("id"):
            cat = emp.categoria_set.get(id=datos.get("id"))
            cat.codigo = datos.get("codigo")
            cat.denominacion = datos.get("denominacion")
            cat.save()
            args['action'] = 'mod'
        else:
            cat = models.Categoria(
                codigo=datos.get("codigo"),
                denominacion=datos.get("denominacion"),
                empresa=emp
            )
            cat.save()
            args['action'] = 'add'
    if request.session.has_key("categoria-del") == 1:
        if request.session["categoria-del"]:
            args['action'] = 'del'
            request.session["categoria-del"] = False

    args.update(csrf(request))
    return render_to_response('categoria/main.html', args, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def del_categoria(request):
    categoria = models.Categoria.objects.get(id=request.POST.get("id"))
    categoria.delete()
    request.session['categoria-del'] = True;

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
