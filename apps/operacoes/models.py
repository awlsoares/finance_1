from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
from apps.configuracoes.models import Conta, CategoriaReceita, CorretoraInvestimento, ContaPrevidenciaPrivada, CategoriaDespesa, CartaoCredito

class Receita(models.Model):

    OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    OPCOES_STATUS= [("Registrado", "Registrado"), ("Efetivado", "Efetivado"),]

    data = models.DateTimeField(default=timezone.now, blank=False)
    valor = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    credito_ja_realizado = models.CharField(max_length=3, choices=OPCOES)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.ForeignKey(CategoriaReceita, on_delete=models.DO_NOTHING, blank=False, null=False)
    conta_credito = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=False, null=False)

    receita_status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='Registrado')
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self):
        return self.descricao

class Despesa(models.Model):

    OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    OPCOES_STATUS= [("Registrado", "Registrado"), ("Efetivado", "Efetivado"),]

    data = models.DateTimeField(default=timezone.now, blank=False)
    valor = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    debito_ja_realizado = models.CharField(max_length=3, choices=OPCOES)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.SET_NULL, blank=False, null=True)
    conta_debito = models.ForeignKey(Conta, on_delete=models.SET_NULL, blank=False, null=True)

    despesa_status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='Registrado')
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    
    def __str__(self):
        return self.descricao

class InvestimentoRendaFixa(models.Model):

    OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    OPCOES_STATUS= [("Registrado", "Registrado"), ("Ativo", "Ativo"), ("Liquidado", "Liquidado"),]
    OPCOES_INVESTIMENTO = [("CDB", "CDB"), ("CRI", "CRI"), ("CRA", "CRA"), ("DEBENTURE", "DEBENTURE"), ("Fundo de RF", "Fundo de RF"), ("LCA", "LCA"), ("LCI", "LCI"), ("POUPANÇA", "POUPANÇA"),("TESOURO", "TESOURO"), ("Outros", "Outros"),]
    OPCOES_RENTABILIDADE = [("PÓS-FIXADA", "PÓS-FIXADA"), ("PRÉ-FIXADA", "PRÉ-FIXADA"),]

    data_investimento = models.DateTimeField(default=timezone.now, blank=False)
    data_vencimento = models.DateTimeField(default=timezone.now, blank=False)
    tipo_investimento_rf = models.CharField(max_length=12, choices=OPCOES_INVESTIMENTO)
    tipo_rentabilidade = models.CharField(max_length=11, choices=OPCOES_RENTABILIDADE)
    corretora = models.ForeignKey(CorretoraInvestimento, on_delete=models.DO_NOTHING, blank=False, null=False)
    valor_investido = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    taxa_negociada = models.CharField(max_length=200, null=False, blank=False)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    taxas_corretagem_aplicacao = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    irpf_aplicacao = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    
    conta_debito = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=False, null=False)
    investimento_debitado_em_conta = models.CharField(max_length=3, choices=OPCOES)
    investimento_status = models.CharField(max_length=10, choices=OPCOES_STATUS)
    
    valor_resgate_liquido = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    taxas_corretagem_resgate = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    irpf_resgate = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    data_resgate = models.DateTimeField(default=timezone.now, blank=False)
    
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.descricao

class InvestimentoRendaVariavel(models.Model):

    OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    OPCOES_STATUS= [("Registrado", "Registrado"), ("Ativo", "Ativo"), ("Liquidado", "Liquidado"),]
    OPCOES_INVESTIMENTO = [("Ações", "Ações"), ("CRIPTO", "CRIPTO"), ("FII", "FII"), ("ETFs", "ETFs"), ("Fundo de RV", "Fundo de RV"), ("Outros", "Outros"),]

    data_investimento = models.DateTimeField(default=timezone.now, blank=False)
    tipo_investimento_rv = models.CharField(max_length=12, choices=OPCOES_INVESTIMENTO)
    corretora = models.ForeignKey(CorretoraInvestimento, on_delete=models.DO_NOTHING, blank=False, null=False)
    valor_investido = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    valor_resgate_liquido = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    quantidade_cotas = models.PositiveIntegerField(blank=False, null=False, default=1)
    preco_medio = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    taxas_corretagem_aplicacao = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    irpf_aplicacao = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    
    conta_debito = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=False, null=False)
    investimento_debitado_em_conta = models.CharField(max_length=3, choices=OPCOES)
    investimento_status = models.CharField(max_length=10, choices=OPCOES_STATUS)
    
    taxas_corretagem_resgate = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    irpf_resgate = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    data_resgate = models.DateTimeField(default=timezone.now, blank=False)

    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.descricao

class InvestimentoPrevidenciaPrivada(models.Model):

    OPCOES= [("Sim", "Sim"), ("Não", "Não"),]
    OPCOES_STATUS= [("Registrado", "Registrado"), ("Efetivado", "Efetivado"), ]

    conta_previdencia = models.ForeignKey(ContaPrevidenciaPrivada, on_delete=models.DO_NOTHING, blank=False, null=False)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    valor_investido = models.DecimalField(blank=False, null=False, default=0.00, max_digits=12, decimal_places=2)
    data_investimento = models.DateTimeField(default=timezone.now, blank=False)
    conta_debito = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=False, null=False)
    investimento_debitado_em_conta = models.CharField(max_length=3, choices=OPCOES)
    investimento_status = models.CharField(max_length=10, choices=OPCOES_STATUS)

    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.descricao

class DespesaCartao(models.Model):

    OPCOES_STATUS= [("Registrada", "Registrada"), ("Paga", "Paga"),]

    data = models.DateField(default=timezone.now, blank=False)
    valor = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    numero_parcelas = models.IntegerField(blank=False, null=False, default=1)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.SET_NULL, blank=False, null=True)
    cartao_selecionado = models.ForeignKey(CartaoCredito, on_delete=models.SET_NULL, blank=False, null=True)
    despesa_status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='Registrada')
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    data_primeira_fatura = models.DateField(default=timezone.now, blank=False)
    
    def __str__(self):
        return self.descricao

class DespesaIndividualizadaCartao(models.Model):

    OPCOES_STATUS= [("Registrada", "Registrada"), ("Paga", "Paga"),]

    data = models.DateField(default=timezone.now, blank=False)
    valor = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    qual_parcela = models.IntegerField(blank=False, null=False, default=1)
    total_parcelas = models.IntegerField(blank=False, null=False, default=1)
    descricao = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.ForeignKey(CategoriaDespesa, on_delete=models.SET_NULL, blank=False, null=True)
    despesa_associada = models.ForeignKey(DespesaCartao, on_delete=models.SET_NULL, blank=False, null=True)
    qual_cartao = models.ForeignKey(CartaoCredito, on_delete=models.SET_NULL, blank=False, null=True)
    despesa_status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='Registrada')
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    qual_fatura = models.DateField(default=timezone.now, blank=False)
    
    def __str__(self):
        return self.descricao
    
class FaturaCartao(models.Model):
    OPCOES_STATUS= [("Aberta", "Aberta"), ("Fechada", "Fechada"), ("Paga", "Paga"),]

    data_fatura = models.DateField(default=timezone.now, blank=False)
    valor = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    encargos = models.DecimalField(blank=False, null=False, default=0.00, max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=200, default='Fatura do mês de...')
    cartao_selecionado = models.ForeignKey(CartaoCredito, on_delete=models.SET_NULL, blank=False, null=True)
    fatura_status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='Aberta')
    data_registro = models.DateTimeField(default=timezone.now, blank=False)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    

    def __str__(self):
        descricao = self.descricao
        vencimento = str(self.data_fatura)
        descricao_fatura = descricao + vencimento

        return descricao_fatura  