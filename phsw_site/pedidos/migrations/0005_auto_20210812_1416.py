# Generated by Django 3.2.6 on 2021-08-12 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20210812_1416'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0004_auto_20210812_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriaitem',
            name='descricao',
            field=models.TextField(default='sem descrição', verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='categoriaitem',
            name='verbose_name',
            field=models.CharField(max_length=15, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='item',
            name='ativado',
            field=models.BooleanField(verbose_name='Ativado'),
        ),
        migrations.AlterField(
            model_name='item',
            name='codigo_barras',
            field=models.CharField(max_length=13, verbose_name='Código de barras'),
        ),
        migrations.AlterField(
            model_name='item',
            name='descricao',
            field=models.TextField(default='sem descrição', verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='item',
            name='unidade',
            field=models.CharField(max_length=10, verbose_name='Unidade'),
        ),
        migrations.AlterField(
            model_name='item',
            name='verbose_name',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='itempedido',
            name='fk_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pedidos.item', verbose_name='Item'),
        ),
        migrations.AlterField(
            model_name='itempedido',
            name='fk_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido', verbose_name='Pedido'),
        ),
        migrations.AlterField(
            model_name='itempedido',
            name='preco_unit',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Preço unitario'),
        ),
        migrations.AlterField(
            model_name='itempedido',
            name='quantidade',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='itempreco',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='itempreco',
            name='fk_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.item', verbose_name='Item'),
        ),
        migrations.AlterField(
            model_name='itempreco',
            name='fk_tabelaPreco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.tabelapreco', verbose_name='Tabela de preço'),
        ),
        migrations.AlterField(
            model_name='itempreco',
            name='preco_unit',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Preço unitario'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_faturamento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data do faturamento'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_pedido',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data do pedido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fk_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.empresa', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fk_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedidos.statuspedido', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fk_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Valor total'),
        ),
        migrations.AlterField(
            model_name='statuspedido',
            name='descricao',
            field=models.TextField(default='sem descrição', verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='statuspedido',
            name='verbose_name',
            field=models.CharField(max_length=15, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='tabelapreco',
            name='verbose_name',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
    ]
