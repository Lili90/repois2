# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
			('1', 'Rol de Sistema'),
			('2', 'Rol de Proyecto'),
		   )

COMPLEXITY_CHOICES = (
			('1', '1'),
			('2', '2'),
			('3', '3'),
			('4', '4'),
			('5', '5'),
			('6', '6'),
			('7', '7'),
			('8', '8'),
			('9', '9'),
			('10', '10'),
		     )

STATUS_CHOICES = (
			('1', 'Pendiente'),
			('2', 'Modificado'),
			('3', 'Revisado'),
		)

PROJECT_STATUS_CHOICES = (
			('1', 'Pendiente'),
			('2', 'Iniciado'),
			('3', 'Terminado'),
			('4', 'Anulado'),
		)

class Permiso(models.Model):
	"""Modelo Permiso"""
	nombre = models.CharField(unique=True, max_length=50)
	categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)

	def __unicode__(self):
		return self.nombre

class Rol(models.Model):
	nombre = models.CharField(unique=True, max_length=50)
	categoria = models.IntegerField(max_length=1, choices=CATEGORY_CHOICES)
	descripcion = models.TextField(null=True, blank=True)
	fecHor_creacion = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)
	usuario_creador = models.ForeignKey(User, null=True)
	permisos = models.ManyToManyField(Permiso, through='RolPermiso')

	def __unicode__(self):
		return self.nombre

class RolPermiso(models.Model):
	"""Modelo Rol Permiso"""
	rol = models.ForeignKey(Rol)
	permiso = models.ForeignKey(Permiso)

class UsuarioRolSistema (models.Model):
	"""Modelo Usuario Rol Sistema"""
	usuario = models.ForeignKey(User)
	rol = models.ForeignKey(Rol)

	class Meta:
		unique_together = [("usuario", "rol")]

class Proyecto(models.Model):
    """Clase que representa un proyecto."""
    nombrelargo = models.CharField(unique=True, max_length=50)
    usuario_lider = models.ForeignKey(User)
    #fase = models.ForeignKey(Fase)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # cronograma = models.FileField(upload_to='cronogramas', null=True, blank=True)
    cantidad = models.IntegerField()
    cant_actual = models.IntegerField(null=True)
    estado = models.IntegerField(max_length=1, choices=PROJECT_STATUS_CHOICES)

    def __unicode__(self):
        return self.nombrelargo

class UsuarioRolProyecto(models.Model):   
    usuario = models.ForeignKey(User)
    rol = models.ForeignKey(Rol, null=True)
    proyecto = models.ForeignKey(Proyecto)

    class Meta:
        unique_together = [("usuario", "rol", "proyecto")]

class Flujo(models.Model):
    """Esta clase representa el flujo para proyecto"""
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    fecHor_creacion = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, editable=False)
    usuario_creador = models.ForeignKey(User, null=True)      
    #proyecto= models.IntegerField()

    def __unicode__(self):
        return self.nombre

