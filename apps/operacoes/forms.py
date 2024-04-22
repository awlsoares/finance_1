from django	import forms
from django.shortcuts import redirect
from django.contrib import messages
from apps.configuracoes.models import Conta, CorretoraInvestimento, ContaPrevidenciaPrivada, CategoriaReceita, CategoriaDespesa, CartaoCredito
from apps.operacoes.models import Receita, InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada, Despesa, DespesaCartao
from datetime import datetime
 
class ReceitaForms(forms.ModelForm):
    class Meta:      
        model = Receita
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'receita_status']
        labels = {
            'data': 'Data do Crédito:',
            'valor': 'Valor (R$):',
            'descricao': 'Descrição:',
            'categoria': 'Categoria:',
            'credito_ja_realizado': 'Valor já Creditado:',
            'conta_credito': 'Conta para Crédito:',
        }

        widgets = {
            'data': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'credito_ja_realizado': forms.Select(attrs={'class':'form-control'}),
            'conta_credito': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['categoria'].queryset = CategoriaReceita.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['conta_credito'].queryset = Conta.objects.filter(proprietario=user).exclude(pk=None)
        
        # Verificar se há uma instância existente para a receita
        if self.instance.id:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            del self.fields['credito_ja_realizado'] # Ocultar o campo 'credito_ja_realizado' do formulário


class DespesaForms(forms.ModelForm):
    class Meta:      
        model = Despesa
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'despesa_status']
        labels = {
            'data': 'Data do Débito:',
            'valor': 'Valor (R$):',
            'descricao': 'Descrição:',
            'categoria': 'Categoria:',
            'debito_ja_realizado': 'Valor já Debitado:',
            'conta_debito': 'Conta para Débito:',
        }

        widgets = {
            'data': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'debito_ja_realizado': forms.Select(attrs={'class':'form-control'}),
            'conta_debito': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['categoria'].queryset = CategoriaDespesa.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['conta_debito'].queryset = Conta.objects.filter(proprietario=user).exclude(pk=None)

        # Verificar se há uma instância existente para a despesa
        if self.instance.id:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            del self.fields['debito_ja_realizado'] # Ocultar o campo 'debito_ja_realizado' do formulário


class InvestimentoRendaFixaForms(forms.ModelForm):
    class Meta:      
        model = InvestimentoRendaFixa
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'investimento_ativo', 'valor_resgate_liquido', 'data_resgate', 'irpf_resgate', 'taxas_corretagem_resgate', 'investimento_status']
        labels = {
            'data_investimento': 'Data da Aplicação: ',
            'data_vencimento': 'Data de Vencimento da Aplicação: ',
            'tipo_investimento_rf': 'Categoria de Investimento: ',
            'tipo_rentabilidade': 'Tipo de Rentabilidade: ',
            'corretora': 'Corretora de Investimentos: ',
            'valor_investido': 'Valor do Investimento (R$):',
            'taxa_negociada': 'Taxa de Rendimento Negociada: ',
            'descricao': 'Descrição: ',
            'taxas_corretagem_aplicacao': 'Taxas de Corretagem na Aplicação (R$):',
            'irpf_aplicacao': 'IRPF na Aplicação (R$): ',
            'conta_debito': 'Conta a ser debitado o Investimento: ',
            'investimento_debitado_em_conta': 'Valor Debitado em Conta:',
        }

        widgets = {
            'data_investimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'data_vencimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'tipo_investimento_rf': forms.Select(attrs={'class':'form-control'}),
            'tipo_rentabilidade': forms.Select(attrs={'class':'form-control'}),
            'corretora': forms.Select(attrs={'class':'form-control'}),
            'valor_investido': forms.NumberInput(attrs={'class':'form-control'}),
            'taxa_negociada': forms.TextInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'taxas_corretagem_aplicacao': forms.NumberInput(attrs={'class':'form-control'}),
            'irpf_aplicacao': forms.NumberInput(attrs={'class':'form-control'}),
            'conta_debito': forms.Select(attrs={'class':'form-control'}),
            'investimento_debitado_em_conta': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['corretora'].queryset = CorretoraInvestimento.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['conta_debito'].queryset = Conta.objects.filter(proprietario=user).exclude(pk=None)

        # Verificar se há uma instância existente para o Investimento
        if self.instance.id:
            self.initial['data_investimento'] = self.instance.data_investimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            self.initial['data_vencimento'] = self.instance.data_vencimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            
            del self.fields['investimento_debitado_em_conta'] # Ocultar o campo 'investimento_debitado_em_conta' do formulário

class ResgateRendaFixaForms(forms.ModelForm):
    class Meta:      
        model = InvestimentoRendaFixa
        fields = ['data_investimento', 'data_vencimento','valor_investido', 'descricao', 'data_resgate', 'valor_resgate_liquido', 'irpf_resgate', 'taxas_corretagem_resgate']
        
        labels = {
            'data_investimento': 'Data do Investimento: ',
            'data_vencimento': 'Data de Vencimento: ',
            'valor_investido': 'Valor Investido: R$ ',
            'descricao': 'Descrição',
            'data_resgate': 'Data do Resgate da Aplicação: ',
            'valor_resgate_liquido': 'Valor Líquido Resgatado (R$)',
            'taxas_corretagem_resgate': 'Taxas de Corretagem no Resgate: ',
            'irpf_resgate': 'IRPF no Resgate (R$): ',
        }

        widgets = {
            'data_investimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', 'readonly': 'readonly'}),
            'data_vencimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', 'readonly': 'readonly'}),
            'valor_investido': forms.NumberInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
            'descricao': forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
            'data_resgate': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'valor_resgate_liquido': forms.NumberInput(attrs={'class':'form-control'}),
            'taxas_corretagem_resgate': forms.NumberInput(attrs={'class':'form-control'}),
            'irpf_resgate': forms.NumberInput(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)                

        # Verificar se há uma instância existente para o Investimento
        if self.instance.id:
            self.initial['data_investimento'] = self.instance.data_investimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            self.initial['data_vencimento'] = self.instance.data_vencimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            self.initial['data_resgate'] = self.instance.data_vencimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            #self.initial['data_resgate'] = self.instance.data_resgate.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
        
class InvestimentoRendaVariavelForms(forms.ModelForm):
    class Meta:      
        model = InvestimentoRendaVariavel
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'investimento_ativo', 'valor_resgate_liquido', 'irpf_resgate', 'taxas_corretagem_resgate', 'data_resgate','investimento_status']
        labels = {
            'data_investimento': 'Data da Aplicação: ',
            'tipo_investimento_rv': 'Categoria de Investimento: ',
            'corretora': 'Corretora de Investimentos: ',
            'valor_investido': 'Valor do Investimento (R$)',
            'quantidade_cotas': 'Quantidade de Cotas: ', 
            'preco_medio': 'Preço Médio (R$)',
            'descricao': 'Descrição: ',
            'taxas_corretagem_aplicacao': 'Taxas de Corretagem: ',
            'irpf_aplicacao': 'IRPF: ',
            'conta_debito': 'Conta a ser debitado o Investimento: ',
            'investimento_debitado_em_conta': 'Valor Debitado em Conta:',
        }

        widgets = {
            'data_investimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'tipo_investimento_rv': forms.Select(attrs={'class':'form-control'}),
            'corretora': forms.Select(attrs={'class':'form-control'}),
            'valor_investido': forms.NumberInput(attrs={'class':'form-control'}),
            'quantidade_cotas': forms.NumberInput(attrs={'class':'form-control'}),
            'preco_medio': forms.NumberInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'taxas_corretagem_aplicacao': forms.NumberInput(attrs={'class':'form-control'}),
            'irpf_aplicacao': forms.NumberInput(attrs={'class':'form-control'}),
            'conta_debito': forms.Select(attrs={'class':'form-control'}),
            'investimento_debitado_em_conta': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['corretora'].queryset = CorretoraInvestimento.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['conta_debito'].queryset = Conta.objects.filter(proprietario=user).exclude(pk=None)

        # Verificar se há uma instância existente para o Investimento
        if self.instance.id:
            self.initial['data_investimento'] = self.instance.data_investimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
            del self.fields['investimento_debitado_em_conta'] # Ocultar o campo 'investimento_debitado_em_conta' do formulário

class ResgateRendaVariavelForms(forms.ModelForm):
    class Meta:      
        model = InvestimentoRendaVariavel
        fields = ['data_investimento', 'valor_investido', 'descricao', 'data_resgate', 'valor_resgate_liquido', 'irpf_resgate', 'taxas_corretagem_resgate']
        
        labels = {
            'data_resgate': 'Data do Resgate da Aplicação: ',
            'valor_resgate_liquido': 'Valor Líquido Resgatado (R$)',
            'taxas_corretagem_resgate': 'Taxas de Corretagem no Resgate: ',
            'irpf_resgate': 'IRPF no Resgate (R$): ',
        }

        widgets = {
            'data_resgate': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'valor_resgate_liquido': forms.NumberInput(attrs={'class':'form-control'}),
            'taxas_corretagem_resgate': forms.NumberInput(attrs={'class':'form-control'}),
            'irpf_resgate': forms.NumberInput(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        data_investimento_original = self.instance.data_investimento.strftime('%d/%m/%Y')
        descricao_original = self.instance.descricao
        valor_investimento_original = self.instance.valor_investido
    
        self.initial['data_investimento'] = data_investimento_original
        self.initial['descricao'] = descricao_original
        self.initial['valor_investido'] = valor_investimento_original        


class InvestimentoPrevidenciaPrivadaForms(forms.ModelForm):
    class Meta:      
        model = InvestimentoPrevidenciaPrivada
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'investimento_status']
        labels = {
            'data_investimento': 'Data da Aplicação: ',
            'conta_previdencia': 'Conta de Previdência Privada: ',
            'valor_investido': 'Valor do Investimento (R$)',
            'descricao': 'Descrição: ',
            'conta_debito': 'Conta a ser debitado o Investimento: ', 
            'investimento_debitado_em_conta': 'Valor Debitado em Conta:',
        }

        widgets = {
            'data_investimento': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),        
            'conta_previdencia': forms.Select(attrs={'class':'form-control'}),
            'valor_investido': forms.NumberInput(attrs={'class':'form-control'}),           
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'conta_debito': forms.Select(attrs={'class':'form-control'}),
            'investimento_debitado_em_conta': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar as contas pertencentes ao usuário autenticado
        self.fields['conta_previdencia'].queryset = ContaPrevidenciaPrivada.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['conta_debito'].queryset = Conta.objects.filter(proprietario=user).exclude(pk=None)


        # Verificar se há uma instância existente para o Investimento
        if self.instance.id:
             self.initial['data_investimento'] = self.instance.data_investimento.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
             del self.fields['investimento_debitado_em_conta'] # Ocultar o campo 'investimento_debitado_em_conta' do formulário


class DespesaCartaoForms(forms.ModelForm):
    class Meta:      
        model = DespesaCartao
        fields = '__all__'
        exclude = ['proprietario', 'data_registro', 'despesa_status', 'data_primeira_fatura']
        labels = {
            'data': 'Data da Despesa:',
            'valor': 'Valor (R$):',
            'numero_parcelas': 'Quantidade de Parcelas:',
            'descricao': 'Descrição:',
            'categoria': 'Categoria:',
            'cartao_selecionado': 'Cartão:',
            #'data_primeira_fatura': 'Fatura (ajustar para mês/ano):'
        }

        widgets = {
            'data': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
            'numero_parcelas': forms.NumberInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'cartao_selecionado': forms.Select(attrs={'class':'form-control'}),
            #'data_primeira_fatura': forms.DateInput(format= '%d/%m/%Y', attrs={'type': 'date', 'class':'form-control', }),
        }

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        # Filtrar os crtões e categorias pertencentes ao usuário autenticado
        self.fields['categoria'].queryset = CategoriaDespesa.objects.filter(proprietario=user).exclude(pk=None)
        self.fields['cartao_selecionado'].queryset = CartaoCredito.objects.filter(proprietario=user).exclude(pk=None)
        self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD

        # Verificar se há uma instância existente para a despesa
        if self.instance.id:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
#             #del self.fields['debito_ja_realizado'] # Ocultar o campo 'debito_ja_realizado' do formulário