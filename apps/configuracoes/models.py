from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Conta(models.Model):

    OPCOES_TIPO = [
        ("Conta Corrente", "Conta Corrente"),
        ("Conta Investimento", "Conta Investimento"),
        ("Conta Poupança", "Conta Poupança"),
        ("Carteira / Cash", "Carteira / Cash"),]

    tipo = models.CharField(max_length=18, choices=OPCOES_TIPO, default='Conta Corrente')
    descricao = models.TextField(max_length=200, null=False, blank=False)
    saldo = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    incluir_saldo_no_dashboard = models.BooleanField(default=True)
    data_registro_conta = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self):
        return self.descricao

class CorretoraInvestimento(models.Model):

    descricao = models.TextField(max_length=200, null=False, blank=False)
    saldo = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    incluir_saldo_no_dashboard = models.BooleanField(default=True)
    data_registro_conta = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self):
        return self.descricao

class ContaPrevidenciaPrivada(models.Model):

    OPCOES_TIPO = [("PGBL", "PGBL"), ("VGBL", "VGBL"),]
    #OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    
    corretora_de_investimento = models.ForeignKey(CorretoraInvestimento, on_delete=models.DO_NOTHING, blank=False, null=False)
    tipo = models.CharField(max_length=18, choices=OPCOES_TIPO, default='PGBL')
    descricao = models.TextField(max_length=200, null=False, blank=False)
    saldo = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    incluir_saldo_no_dashboard = models.BooleanField(default=True)
    data_registro_previdencia = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.descricao

class CategoriaReceita(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self): 
        return self.descricao

class CategoriaDespesa(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self): 
        return self.descricao
    
class CartaoCredito(models.Model):
    OPCOES_BANDEIRA = [
        ("Visa", "Visa"),
        ("Master", "Master"),
        ("Elo", "Elo"),
        ("Diners", "Diners"),
        ("Amex", "Amex"),
        ("Outros", "Outros"),]

    OPCOES_DIA = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), 
                  (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13),
                  (14, 14), (15 ,15), (16, 16), (17, 17), (18, 18), (19, 19),
                  (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                  (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31),]
    
    bandeira = models.CharField(max_length=18, choices=OPCOES_BANDEIRA, default='')
    descricao = models.TextField(max_length=200, null=False, blank=False)
    limite = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    limite_disponivel = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)


    incluir_saldo_no_dashboard = models.BooleanField(default=True)
    dia_vencimento_fatura = models.IntegerField(choices=OPCOES_DIA, default=1)
    dia_fechamento_fatura = models.IntegerField(choices=OPCOES_DIA, default=1)
    data_registro_cartao = models.DateTimeField(default=timezone.now, blank=False)
    local_debito_fatura = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=False, null=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.descricao