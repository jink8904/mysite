from builtins import print
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
import json
# from XlsxWriter import xlsxwriter
# users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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
