# -*- coding: utf-8 -*-
import base64
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context
from SGPA.apps.usuario.forms import UsuariosForm
from django.core.mail import EmailMultiAlternatives # Enviamos HTML
from django.contrib.auth.models import User
import django
from SGPA.settings import URL_LOGIN
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse, Http404
# Paginacion en Django
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required
from django.template import *
from django.contrib import*
from django.template.loader import get_template
from django.forms.formsets import formset_factory
from SGPA.apps.usuario.forms import *
from SGPA.apps.usuario.models import *
from SGPA.apps.usuario.helper import *

def crearUsuario_view(request):
	form = UsuariosForm()
	if request.method == "POST":
		form = UsuariosForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=username,email=email,password=password_one)
			u.save() # Guardar el objeto
			return HttpResponseRedirect("/admin")
			#return render_to_response('usuario/usuarios.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render_to_response('usuario/crearUsuario.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('usuario/crearUsuario.html',ctx,context_instance=RequestContext(request))

def lista(request, tipo):
    """Metodo de prueba para listar"""
    user = User.objects.get(username=request.user.username)
    if tipo == 'usuarios':
        lista = User.objects.all()
    else:
        return render_to_response('error.html');
    return render_to_response('lista.html',{'lista':lista, 'user':user, 'tipo':tipo})

@login_required
def admin_usuarios(request):
    """Administracion general de usuarios"""
    '''Ya esta la validacion de permisos en este'''
    user = User.objects.get(username=request.user.username)

    lista = User.objects.all().order_by("id")
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            palabra = form.cleaned_data['filtro']
            lista = User.objects.filter(Q(username__icontains = palabra) | Q(first_name__icontains = palabra) | Q(last_name__icontains = palabra)).order_by('id')
            paginas = form.cleaned_data['paginas']
            request.session['nro_items'] = paginas
            paginator = Paginator(lista, int(paginas))
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                pag = paginator.page(page)
            except (EmptyPage, InvalidPage):
                pag = paginator.page(paginator.num_pages)
            return render_to_response('usuario/usuarios.html',{'pag': pag,
                                                               'form': form,
                                                               'lista':lista,
                                                               'user':user})
    else:
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if not 'nro_items' in request.session:
            request.session['nro_items'] = 5
        paginas = request.session['nro_items']
        paginator = Paginator(lista, int(paginas))
        try:
            pag = paginator.page(page)
        except (EmptyPage, InvalidPage):
            pag = paginator.page(paginator.num_pages)
        form = FilterForm(initial={'paginas': paginas})
    return render_to_response('usuario/usuarios.html',{ 'pag':pag,
                                                               'form': form,
                                                               'lista':lista,
                                                               'user':user})

