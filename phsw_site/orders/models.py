from django.db import models
from django.utils import timezone
from .utils import image_resize


class Item(models.Model):
    item_code = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE, verbose_name="Categoria")
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    description = models.TextField(default="sem descrição", verbose_name="Descrição")
    unit = models.CharField(max_length=10, verbose_name="Unidade")
    bar_code = models.CharField(max_length=13, verbose_name="Código de barras")
    active = models.BooleanField(verbose_name='Ativado')
    image = models.ImageField(default="images/items/defaultimage.jpeg", upload_to='images/items/')

    def __str__(self):
        return f'{self.item_code}'

    class Meta:
        verbose_name_plural = 'Itens'

    def save(self, *args, **kwargs):
        if self.image:
            image_resize(self.image, 115, 76.24)
        super().save(*args, **kwargs)


class ItemCategory(models.Model):
    category_code = models.CharField(max_length=8, unique=True)
    description = models.TextField(default="sem descrição", verbose_name="Descrição")
    verbose_name = models.CharField(max_length=15, verbose_name="Nome")

    def __str__(self):
        return f'Categoria: {self.verbose_name}'


class PriceItem(models.Model):
    class Meta:
        unique_together = (('pricetable', 'item'),)
    pricetable = models.ForeignKey('PriceTable', on_delete=models.CASCADE, related_name='price_items', verbose_name="Tabela de preço")
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Item")
    price_unit = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data")


class PriceTable(models.Model):
    table_code = models.CharField(max_length=7, unique=True)
    verbose_name = models.CharField(max_length=50, verbose_name="Nome")
    items = models.ManyToManyField(Item, through='PriceItem')

    def __str__(self):
        return f'{self.table_code}'


class Order(models.Model):
    status_choices = (
        ("0", "Digitação"),
        ("1", "Transferido"),
        ("2", "Registrado"),
        ("3", "Faturado"),
        ("5", "Entregue"),
        ("9", "Cancelado")
    )
    company = models.ForeignKey('base.Company', on_delete=models.CASCADE, verbose_name="Empresa")
    user = models.ForeignKey('base.User', on_delete=models.PROTECT, verbose_name="Usuário")
    status = models.CharField(max_length=1, choices=status_choices)
    # numero_nota = formato(' 999.999.999')
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Data do pedido")
    billing_date = models.DateTimeField(blank=True, null=True, verbose_name="Data do faturamento")
    order_amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Valor total")

    def __str__(self):
        return f'Pedido N. {self.pk}'


class OrderedItem(models.Model):
    class Meta:
        unique_together = (('order', 'item'),)
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Pedido")
    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, verbose_name="Item")
    quantity = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Quantidade")
    unit_price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Preço unitario")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data")
