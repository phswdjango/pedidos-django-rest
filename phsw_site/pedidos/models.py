from django.db import models
from django.utils import timezone
from .utils import image_resize


class Item(models.Model):
    codigo_item = models.CharField(max_length=15, unique=True)
    fk_categoria = models.ForeignKey('CategoriaItem', on_delete=models.CASCADE, verbose_name="Categoria")
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
    unidade = models.CharField(max_length=10, verbose_name="Unidade")
    codigo_barras = models.CharField(max_length=13, verbose_name="Código de barras")
    ativado = models.BooleanField(verbose_name='Ativado')  # zero(desativado), Um(ativado)
    imagem = models.ImageField(default="imagens/itens/defaultimage.jpeg", upload_to='imagens/itens/')

    def __str__(self):
        return f'{self.verbose_name} - {self.codigo_item}'

    class Meta:
        verbose_name_plural = 'Itens'

    def save(self, *args, **kwargs):
        if self.imagem:
            image_resize(self.imagem, 115, 76.24)
        super().save(*args, **kwargs)


class CategoriaItem(models.Model):
    codigo_categoria = models.CharField(max_length=8, unique=True)
    descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
    verbose_name = models.CharField(max_length=15, verbose_name="Nome")

    def __str__(self):
        return f'Categoria: {self.verbose_name}'


class ItemPreco(models.Model):  # tabela intermediária
    class Meta:
        unique_together = (('fk_tabelaPreco', 'fk_item'),)
    fk_tabelaPreco = models.ForeignKey('TabelaPreco', on_delete=models.CASCADE, related_name='itens_preco', verbose_name="Tabela de preço")
    fk_item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='item_code', verbose_name="Item")
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")


class TabelaPreco(models.Model):
    codigo_tabela = models.CharField(max_length=7, unique=True)
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    itens = models.ManyToManyField(Item, through='ItemPreco')

    def __str__(self):
        return f'{self.verbose_name} - {self.codigo_tabela}'


class Pedido(models.Model):
    status_choices = (
        ("0", "Digitação"),
        ("1", "Transferido"),
        ("2", "Registrado"),
        ("3", "Faturado"),
        ("5", "Entregue"),
        ("9", "Cancelado")
    )
    fk_empresa = models.ForeignKey('base.Empresa', on_delete=models.CASCADE, verbose_name="Empresa")
    fk_usuario = models.ForeignKey('base.User', on_delete=models.PROTECT, verbose_name="Usuário")
    # fk_status = models.ForeignKey('StatusPedido', on_delete=models.PROTECT, verbose_name="Status")
    status = models.CharField(max_length=1, choices=status_choices)
    # numero_nota = formato(' 999.999.999')
    data_pedido = models.DateTimeField(default=timezone.now, verbose_name="Data do pedido")
    data_faturamento = models.DateTimeField(blank=True, null=True, verbose_name="Data do faturamento")
    valor_total = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Valor total")

    def __str__(self):
        return f'Pedido N. {self.pk}'


# class StatusPedido(models.Model):
#     descricao = models.TextField(default="sem descrição", verbose_name="Descrição")
#     verbose_name = models.CharField(max_length=15, verbose_name="Nome")
#
#     def __str__(self):
#         return f'Status: {self.verbose_name}'


class ItemPedido(models.Model):
    class Meta:
        unique_together = (('fk_pedido', 'fk_item'),)
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    fk_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, verbose_name="Pedido")
    fk_item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, verbose_name="Item")
    quantidade = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Quantidade")
    preco_unit = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")


