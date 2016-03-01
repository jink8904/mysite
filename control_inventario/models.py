from pickle import TRUE
from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    anno_inicio = models.IntegerField()
    ruc = models.IntegerField(unique=TRUE)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    codigo = models.IntegerField(unique=TRUE)
    denominacion = models.CharField(max_length=50)
    empresa = models.ManyToManyField(Empresa)

    def __str__(self):
        return self.denominacion


class TipoProducto(models.Model):
    codigo = models.IntegerField(unique=TRUE)
    denominacion = models.CharField(max_length=50)

    def __str__(self):
        return self.denominacion

    class Admin:
        pass


class UnidadProducto(models.Model):
    codigo = models.IntegerField(unique=TRUE)
    denominacion = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return self.denominacion

    class Admin:
        pass


class Producto(models.Model):
    codigo = models.IntegerField(unique=TRUE)
    nombre = models.CharField(max_length=30)
    nombre_reducido = models.CharField(max_length=30)
    tipo = models.ForeignKey(TipoProducto)
    unidad = models.ForeignKey(UnidadProducto)
    categoria = models.ForeignKey(Categoria)
    empresa = models.ManyToManyField(Empresa)


class TipoId(models.Model):
    codigo = models.IntegerField(unique=TRUE)
    denominacion = models.CharField(max_length=50)

    def __str__(self):
        return self.denominacion

    class Admin:
        pass


class Proveedor(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    identificador = models.IntegerField(unique=TRUE)
    tipo_id = models.ForeignKey(TipoId)
    empresa = models.ManyToManyField(Empresa)


class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    identificador = models.IntegerField(unique=TRUE)
    tipo_id = models.ForeignKey(TipoId)
    empresa = models.ManyToManyField(Empresa)


class Inventario(models.Model):
    costo_unitario = models.DecimalField(decimal_places=4, max_digits=6)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    empresa = models.ForeignKey(Empresa)


class TipoComprobante(models.Model):
    codigo = models.IntegerField()
    denominacion = models.CharField(max_length=50)


class Compra(models.Model):
    fecha = models.DateField()
    serie = models.IntegerField()
    numero = models.IntegerField()
    tipo_comprobante = models.ForeignKey(TipoComprobante)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    igv = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor)
    empresa = models.ForeignKey(Empresa)


class DetalleCompra(models.Model):
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    valor_venta = models.DecimalField(max_digits=6, decimal_places=2)
    igv = models.DecimalField(max_digits=6, decimal_places=2)
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    producto = models.ForeignKey(Producto)
    compra = models.ForeignKey(Compra)


class Venta(models.Model):
    fecha = models.DateField()
    serie = models.IntegerField()
    numero = models.IntegerField()
    tipo_comprobante = models.ForeignKey(TipoComprobante)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    igv = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    cliente = models.ForeignKey(Cliente)
    empresa = models.ForeignKey(Empresa)


class DetalleVenta(models.Model):
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    valor_venta = models.DecimalField(max_digits=6, decimal_places=2)
    igv = models.DecimalField(max_digits=6, decimal_places=2)
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    producto = models.ForeignKey(Producto)
    venta = models.ForeignKey(Venta)


class TipoOperacion(models.Model):
    denominacion = models.CharField(max_length=50)
