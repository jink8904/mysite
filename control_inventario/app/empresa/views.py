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
    empresa = models.Empresa.objects.get(ruc=request.POST.get("ruc"))
    empresa.delete();
    return HttpResponseRedirect('/empresa')

def select_periodo(request):
    request.session['mes'] = request.POST.get("periodo")
    return HttpResponseRedirect('/');

