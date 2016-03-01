__author__ = 'Julio'
from django import forms
from control_inventario import models


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = models.Empresa


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = models.Categoria


class ProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
