# Generated by Django 4.2.6 on 2024-01-06 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0017_alter_categoriadespesa_proprietario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operacoes', '0013_alter_investimentoprevidenciaprivada_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='receita_status',
            field=models.CharField(choices=[('Registrado', 'Registrado'), ('Efetivado', 'Efetivado')], default='Registrado', max_length=10),
        ),
        migrations.AlterField(
            model_name='investimentoprevidenciaprivada',
            name='investimento_status',
            field=models.CharField(choices=[('Registrado', 'Registrado'), ('Efetivado', 'Efetivado')], default='Registrado', max_length=10),
        ),
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('debito_ja_realizado', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], max_length=3)),
                ('descricao', models.CharField(max_length=200)),
                ('despesa_status', models.CharField(choices=[('Registrado', 'Registrado'), ('Efetivado', 'Efetivado')], default='Registrado', max_length=10)),
                ('data_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='configuracoes.categoriadespesa')),
                ('conta_debito', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='configuracoes.conta')),
                ('proprietario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]