# Generated by Django 4.2.6 on 2023-12-19 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuracoes', '0014_alter_cartaocredito_local_debito_fatura_and_more'),
        ('operacoes', '0003_alter_receita_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receita',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.categoriareceita'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='conta_credito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.conta'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='proprietario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='InvestimentoRendaVariavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_investimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_investimento_rv', models.CharField(choices=[('Ações', 'Ações'), ('CRIPTO', 'CRIPTO'), ('FII', 'FII'), ('ETFs', 'ETFs'), ('Fundo de RV', 'Fundo de RV'), ('Outros', 'Outros')], default='Ações', max_length=12)),
                ('valor_investido', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('quantidade_cotas', models.PositiveIntegerField(default=1)),
                ('preco_medio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('descricao', models.TextField(max_length=200)),
                ('taxas_corretagem', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('irpf', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('investimento_ativo', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Sim', max_length=3)),
                ('data_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('conta_debito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.conta')),
                ('corretora', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.corretorainvestimento')),
                ('proprietario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestimentoRendaFixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_investimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_vencimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_investimento_rf', models.CharField(choices=[('CDB', 'CDB'), ('CRI', 'CRI'), ('CRA', 'CRA'), ('DEBENTURE', 'DEBENTURE'), ('Fundo de RF', 'Fundo de RF'), ('LCA', 'LCA'), ('LCI', 'LCI'), ('POUPANÇA', 'POUPANÇA'), ('TESOURO', 'TESOURO'), ('Outros', 'Outros')], default='CDB', max_length=12)),
                ('tipo_rentabilidade', models.CharField(choices=[('PÓS-FIXADA', 'PÓS-FIXADA'), ('PRÉ-FIXADA', 'PRÉ-FIXADA')], default='PÓS-FIXADA', max_length=11)),
                ('valor_investido', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('taxa_negociada', models.TextField(max_length=200)),
                ('descricao', models.TextField(max_length=200)),
                ('taxas_corretagem', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('irpf', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('investimento_ativo', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Sim', max_length=3)),
                ('data_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('conta_debito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.conta')),
                ('corretora', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.corretorainvestimento')),
                ('proprietario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestimentoPrevidenciaPrivada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=200)),
                ('valor_investido', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('data_investimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('conta_debito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.conta')),
                ('conta_previdencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='configuracoes.contaprevidenciaprivada')),
                ('proprietario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]