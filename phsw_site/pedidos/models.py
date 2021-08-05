from django.db import models
from django.utils import timezone


class Item(models.Model):
    id_item = models.CharField(max_length=15, primary_key=True)
    fk_categoria = models.ForeignKey('CategoriaItem', on_delete=models.CASCADE)
    verbose_name = models.CharField(max_length=50)
    descricao = models.TextField(default="sem descrição")
    unidade = models.CharField(max_length=10)
    codigo_barras = models.IntegerField()
    ativado = models.BooleanField()  # zero(desativado), Um(ativado)
    # imagem = models.ImageField

    def __str__(self):
        return f'Item: {self.verbose_name}'


class ItemPreco(models.Model):  # tabela intermediária
    class Meta:
        unique_together = (('fk_tabelaPreco', 'fk_item'),)
    fk_tabelaPreco = models.ForeignKey('TabelaPreco', on_delete=models.CASCADE)
    fk_item = models.ForeignKey('Item', on_delete=models.CASCADE)
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)


class TabelaPreco(models.Model):
    id_tabela = models.CharField(max_length=7, primary_key=True)
    verbose_name = models.CharField(max_length=50)
    itens = models.ManyToManyField(Item, through='ItemPreco')

    def __str__(self):
        return f'Tabela: {self.verbose_name}'


class Pedido(models.Model):
    fk_empresa = models.ForeignKey('base.Empresa', on_delete=models.CASCADE)
    fk_usuario = models.ForeignKey('Item', on_delete=models.PROTECT)
    fk_status = models.ForeignKey('StatusPedido', on_delete=models.PROTECT)
    # numero_nota = formato(' 999.999.999')
    data_pedido = models.DateTimeField(default=timezone.now)
    data_faturamento = models.DateTimeField(blank=True, null=True)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2)


class StatusPedido(models.Model):
    descricao = models.TextField(default="sem descrição")
    verbose_name = models.CharField(max_length=15)

    def __str__(self):
        return f'Status: {self.verbose_name}'


class ItemPedido(models.Model):
    class Meta:
        unique_together = (('fk_pedido', 'fk_item'),)

    fk_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    fk_item = models.ForeignKey('Item', on_delete=models.DO_NOTHING)
    quantidade = models.DecimalField(max_digits=11, decimal_places=2)
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2)


class CategoriaItem(models.Model):
    id_categoria = models.CharField(max_length=8, primary_key=True)
    descricao = models.TextField(default="sem descrição")
    verbose_name = models.CharField(max_length=15)

    def __str__(self):
        return f'Categoria: {self.verbose_name}'

