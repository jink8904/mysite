from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
import json
# users
from django.contrib.auth.decorators import login_required


@login_required(login_url='/ingresar')
def empresa(request):
    empresa_list = models.Empresa.objects.values()
    datos = request.POST
    args = {}

    if datos:
        if datos.get("id"):
            emp = models.Empresa.objects.get(id=datos.get("id"))
            emp.nombre = datos.get("nombre")
            emp.anno_inicio = datos.get("anno_inicio")
            emp.ruc = datos.get("ruc")
            emp.direccion = datos.get("direccion")
            emp.save()
            args['action'] = "mod"
        else:
            form = forms.EmpresaForm(request.POST)
            if form.is_valid():
                args['action'] = "add"
                form.save()
            else:
                args['action'] = "error"

    if request.session.has_key("empresa-del") == 1:
        if request.session["empresa-del"]:
            args['action'] = 'del'
            request.session["empresa-del"] = False
    args.update(csrf(request))
    args['empresa_list'] = empresa_list
    return render_to_response('empresa/main.html', args, context_instance=RequestContext(request))


def select_empresa(request):
    datos = request.POST
    request.session['empresa'] = {
        "ruc": datos.get("empresa[ruc]"),
        "nombre": datos.get("empresa[nombre]"),
        "id": datos.get("empresa[id]"),
        "direccion": datos.get("empresa[direccion]"),
        "anno_inicio": datos.get("empresa[anno_inicio]"),
    }
    request.session['mes'] = datos.get("mes")
    json_data = json.dumps({"success": True})
    return HttpResponse(json_data, mimetype="application/json")


@login_required(login_url='/ingresar')
def del_empresa(request):
    empresa = models.Empresa.objects.get(id=request.POST.get("id"))
    empresa.delete()
    request.session['empresa-del'] = True

    args = {}
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")


def select_periodo(request):
    print(request.POST.get("periodo"))
    request.session['mes'] = request.POST.get("periodo")
    return HttpResponseRedirect('/')
