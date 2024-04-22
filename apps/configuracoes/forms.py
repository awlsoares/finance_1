from django	import forms
from apps.configuracoes.models import Conta, CorretoraInvestimento, ContaPrevidenciaPrivada, CategoriaReceita, CategoriaDespesa, CartaoCredito

class ContaForms(forms.ModelForm):
    class Meta:
        model = Conta
        fields = '__all__' # escolhe quais campos aparecerão: Ex: fields = ['tipo', 'descricao', 'saldo', 'incluir_saldo_no_dash_board']
        exclude = ['data_registro_conta', 'proprietario'] # qual campo não aparecerá no formulário.
        labels = {
            'descricao': 'Descrição da Conta:',
            'saldo': 'Saldo (R$)',
            'tipo': 'Tipo de Conta:',
            'incluir_saldo_no_dashboard': 'Incluir no Saldo Total:'
        }

        widgets = {
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'saldo': forms.NumberInput(attrs={'class':'form-control'}),
            'incluir_saldo_no_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CorretoraForms(forms.ModelForm):
    class Meta:
        model = CorretoraInvestimento
        fields = '__all__' # escolhe quais campos aparecerão: Ex: fields = ['tipo', 'descricao', 'saldo', 'incluir_saldo_no_dash_board']
        exclude = ['data_registro_conta', 'proprietario'] # qual campo não aparecerá no formulário.
        labels = {
            'descricao': 'Descrição da Corretora:',
            'saldo': 'Saldo (R$)',
            'incluir_saldo_no_dashboard': 'Incluir no Saldo Total:'
        }

        widgets = {
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'saldo': forms.NumberInput(attrs={'class':'form-control'}),
            'incluir_saldo_no_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ContaPrevidenciaPrivadaForms(forms.ModelForm):
    class Meta:
        model = ContaPrevidenciaPrivada
        fields = '__all__' # escolhe quais campos aparecerão: Ex: fields = ['tipo', 'descricao', 'saldo', 'incluir_saldo_no_dash_board']
        exclude = ['data_registro_previdencia', 'proprietario'] # qual campo não aparecerá no formulário.
        labels = {
            'corretora_de_investimento': 'Corretora de Investimento: ',
            'tipo': 'Tipo de Previdência Privada:',
            'descricao': 'Descrição da Conta de Previdência:',
            'saldo': 'Saldo (R$)',
            'incluir_saldo_no_dashboard': 'Incluir no Saldo Total de Investimentos:'
        }

        widgets = {
            'corretora_de_investimento': forms.Select(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'saldo': forms.NumberInput(attrs={'class':'form-control'}),
            'incluir_saldo_no_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CategoriaReceitaForms(forms.ModelForm):
    class Meta:
        model = CategoriaReceita
        fields = '__all__'
        exclude = ['proprietario']
        labels = {'descricao': 'Nome da Categoria de Receita:'}
        widgets = {'descricao': forms.TextInput(attrs={'class':'form-control'}),}
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CategoriaDespesaForms(forms.ModelForm):
    class Meta:
        model = CategoriaDespesa
        fields = '__all__'
        exclude = ['proprietario']
        labels = {'descricao': 'Nome da Categoria de Despesa:'}
        widgets = {'descricao': forms.TextInput(attrs={'class':'form-control'}),}
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class CartaoCreditoForms(forms.ModelForm):
    class Meta:
        model = CartaoCredito
        fields = '__all__'
        exclude = ['proprietario', 'data_registro_cartao',]
        labels = {
            'bandeira': 'Bandeira:',
            'descricao': 'Descrição:',
            'limite': 'Limite (R$)',
            'incluir_saldo_no_dashboard': 'Incluir no Dashboard:',
            'dia_vencimento_fatura': 'Dia de Vencimento da Fatura (1 a 31):',
            'dia_fechamento_fatura': 'Dia de Fechamento da Fatura (1 a 31):',
            'local_debito_fatura': 'Local do Débito da Fatura'
        }

        widgets = {
            'bandeira': forms.Select(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'limite': forms.NumberInput(attrs={'class':'form-control'}),
            'incluir_saldo_no_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dia_vencimento_fatura': forms.Select(attrs={'class':'form-control'}),
            'dia_fechamento_fatura': forms.Select(attrs={'class':'form-control'}),
            'local_debito_fatura': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['local_debito_fatura'].queryset = Conta.objects.filter(proprietario=user)
        del self.fields['limite_disponivel'] # Ocultar o campo 'investimento_debitado_em_conta' do formulário