# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from SGPA.apps.usuario.models import *
from SGPA.apps.usuario.helper import *
import datetime
import django
django.setup()

class FilterForm(forms.Form):
    """
    Clase para el formulario Busqueda y Paginacion de UserHistory
    """
    filtro = forms.CharField(max_length = 30, label = 'BUSCAR', required=False)
    paginas = forms.CharField(max_length=2, widget=forms.Select(choices=(('5','5'),('10','10'),('15','15'),('20','20'))), label='MOSTRAR')

class UserHistoryForm(forms.Form):
    """
    Clase para el formulario de UserHistory
    """
    nombre = forms.CharField(max_length=50, label='NOMBRE')
    descripcion = forms.CharField(max_length=500, label='DESCRIPCION')
    estado = forms.CharField(max_length=12, widget=forms.Select(choices=ESTADO_CHOICES), label = 'ESTADO')
    valor_tecnico = forms.IntegerField(label='VALOR TECNICO')
    valor_negocio = forms.IntegerField(label='VALOR NEGOCIO')
    tiempo_estimado = forms.IntegerField(label='TIEMPO ESTIMADO')
    encargado = forms.ModelChoiceField(queryset=User.objects.filter())
    #usuario_lider = forms.ModelChoiceField(queryset=User.objects.all())
    proyecto = Proyecto()

    def __init__(self, proyecto, *args, **kwargs):
        super(UserHistoryForm, self).__init__(*args, **kwargs)
        self.proyecto = proyecto
        urp = UsuarioRolProyecto.objects.filter(proyecto = proyecto)
        listUser = []
        for rec in urp:
            if not rec.usuario.id in listUser:
                listUser.append(rec.usuario.id)
        self.fields['encargado'].queryset = User.objects.filter(Q(id__in = listUser))

class ModUserHistoryForm(forms.Form):
    """
    Clase para el formulario de modificar User History
    """
    estado = forms.CharField(max_length=12, widget=forms.Select(choices=ESTADO_CHOICES), label = 'ESTADO')
    tiempo_estimado = forms.IntegerField(label='TIEMPO ESTIMADO')