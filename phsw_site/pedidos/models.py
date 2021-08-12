from django.db import models
from django.utils import timezone


class Item(models.Model):
    id_item = models.CharField(max_length=15, primary_key=True)
    fk_categoria = models.ForeignKey('CategoriaItem', on_delete=models.CASCADE, verbose_name="Categoria")
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
    unidade = models.CharField(max_length=10, verbose_name="Unidade")
    codigo_barras = models.CharField(max_length=13, verbose_name="Código de barras")
    ativado = models.BooleanField(verbose_name='Ativado')  # zero(desativado), Um(ativado)
    # imagem = models.ImageField

    def __str__(self):
        return f'Item: {self.verbose_name}'


class ItemPreco(models.Model):  # tabela intermediária
    class Meta:
        unique_together = (('fk_tabelaPreco', 'fk_item'),)
    fk_tabelaPreco = models.ForeignKey('TabelaPreco', on_delete=models.CASCADE, verbose_name="Tabela de preço")
    fk_item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Item")
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")


class TabelaPreco(models.Model):
    id_tabela = models.CharField(max_length=7, primary_key=True)
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    itens = models.ManyToManyField(Item, through='ItemPreco')

    def __str__(self):
        return f'Tabela: {self.verbose_name}'


class Pedido(models.Model):
    fk_empresa = models.ForeignKey('base.Empresa', on_delete=models.CASCADE, verbose_name="Empresa")
    fk_usuario = models.ForeignKey('base.User', on_delete=models.PROTECT, verbose_name="Usuário")
    fk_status = models.ForeignKey('StatusPedido', on_delete=models.PROTECT, verbose_name="Status")
    # numero_nota = formato(' 999.999.999')
    data_pedido = models.DateTimeField(default=timezone.now, verbose_name="Data do pedido")
    data_faturamento = models.DateTimeField(blank=True, null=True, verbose_name="Data do faturamento")
    valor_total = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Valor total")


class StatusPedido(models.Model):
    descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
    verbose_name = models.CharField(max_length=15, verbose_name="Nome")

    def __str__(self):
        return f'Status: {self.verbose_name}'


class ItemPedido(models.Model):
    class Meta:
        unique_together = (('fk_pedido', 'fk_item'),)

    fk_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, verbose_name="Pedido")
    fk_item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, verbose_name="Item")
    quantidade = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Quantidade")
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")


class CategoriaItem(models.Model):
    id_categoria = models.CharField(max_length=8, primary_key=True)
    descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
    verbose_name = models.CharField(max_length=15, verbose_name="Nome")

    def __str__(self):
        return f'Categoria: {self.verbose_name}'

