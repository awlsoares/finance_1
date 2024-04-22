from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, date, datetime, timezone
from dateutil.relativedelta import relativedelta
from apps.configuracoes.models import Conta, CategoriaDespesa, CartaoCredito
from apps.operacoes.models import DespesaCartao, DespesaIndividualizadaCartao, FaturaCartao
from apps.operacoes.forms import DespesaForms, DespesaCartaoForms
from django.db.models import Case, Value, When, CharField

# ---------------------- Despesas Cartão de Crédito --------------------------

# Realizar o registro de uma nova fatura do cartão com status 'Aberta'.
def registrar_fatura(usuario, cartao, data_vencimento):
    
    data_mes = data_vencimento.month
    data_ano = data_vencimento.year

    fatura = FaturaCartao(
        data_fatura = data_vencimento, 
        valor = 0,
        encargos = 0,
        descricao = 'Fatura de ' + str(data_vencimento),
        cartao_selecionado = cartao,
        fatura_status = 'Aberta',
        data_registro = datetime.now(),              
        proprietario = usuario)    
    fatura.save()
    print(f'Usuário: {usuario}. Cartão: {cartao}. Data Vencimento: {data_mes}/{data_ano}.')

# Função para selecionar a fatura e alterar o status para 'Fechada'
def fechar_fatura(fatura_id):
    fatura = get_object_or_404(FaturaCartao, id=fatura_id)
    fatura.fatura_status = 'Fechada'
    fatura.save()
    #messages.success(request, 'Fatura Fechada com sucesso.')
    return redirect('index')

# Verifica e obtem as faturas por status
def obter_fatura_status(usuario, cartao_id, status):
    return FaturaCartao.objects.filter(proprietario=usuario, cartao_selecionado=cartao_id, fatura_status=status)

# Verifica e obtem as faturas por status e por data de vencimento
def obter_fatura_status_vencimento(usuario, cartao_id, status, vencimento):
    return FaturaCartao.objects.filter(proprietario=usuario, cartao_selecionado=cartao_id, fatura_status=status, data_fatura=vencimento)

# Verifica e obtem as faturas por cartao
def obter_fatura_cartao(usuario, cartao_id):
    return FaturaCartao.objects.filter(proprietario=usuario, cartao_selecionado=cartao_id)


# Recebe uma despesa do cartão e gera as despesas parceladas (qtd parcelas >= 1).
def criar_despesa_individualizada(despesa_cartao_id):
    pass

def escolher_cartao(request):
    cartoes = CartaoCredito.objects.filter(proprietario=request.user)

    if request.method == 'POST':
        cartao_escolhido = request.POST.get('cartao_selecionado')
        cartao_escolhido = get_object_or_404(CartaoCredito, id=cartao_escolhido)
        print("Cartão escolhido: ", cartao_escolhido)
        # Faça o que precisa com o cartão escolhido

    return render(request, 'cartao/cartao-escolher.html', {'cartoes': cartoes })


# Cria uma despesa no cartão
def cartao_despesa_nova(request):

    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    opcao_de_cartao = CartaoCredito.objects.filter(proprietario=request.user)
    cartao_escolhido = escolher_cartao(request, opcao_de_cartao)
    print("Cartão Escolhido: ",cartao_escolhido)

    if request.method == 'POST':
        form = DespesaCartaoForms(request.user, request.POST)
        if form.is_valid():
            # 1) Calcula a data de vencimento da fatura que é esperado que esteja Aberta baseado na data atual, na data de fechamento e vencimento da fatura.
            # 2) Usa essa data para inicializar o campo 'data_fatura_ajusta' no Formulário.

            nova_despesa = form.save(commit=False)
            print("Nome da Despesa: ", nova_despesa)
            nova_despesa.proprietario = request.user
            qual_fatura = request.POST.get('data_fatura_ajustada')
            cartao = get_object_or_404(CartaoCredito, id=nova_despesa.cartao_selecionado_id)
            
            data_vencimento_cartao = (qual_fatura + '-' + str(cartao.dia_vencimento_fatura))
            data_vencimento_cartao = (datetime.strptime(data_vencimento_cartao, '%Y-%m-%d')).date()
            data_fechamento_cartao = (qual_fatura + '-' + str(cartao.dia_fechamento_fatura))
            data_fechamento_cartao = (datetime.strptime(data_fechamento_cartao, '%Y-%m-%d')).date()
           
            faturas = obter_fatura_cartao(request.user, nova_despesa.cartao_selecionado_id)
            qtd_fatura = len(faturas)

            if len(obter_fatura_cartao(request.user, nova_despesa.cartao_selecionado_id)) == 0: # Verifica se NÃO existe fatura para o cartão.
                cartao = CartaoCredito.objects.get(pk=nova_despesa.cartao_selecionado_id)
                registrar_fatura(nova_despesa.proprietario, cartao, data_vencimento_cartao) # cria uma nova fatura para o cartão.             
            else: # Existe 1 ou mais faturas registradas para o cartão.
                # Verifica se existe fatura aberta para o cartão.
                faturas_abertas = obter_fatura_status(request.user, nova_despesa.cartao_selecionado_id, 'Aberta')
                # Verifica se existe fatura fechada para o cartão.
                faturas_fechadas = obter_fatura_status(request.user, nova_despesa.cartao_selecionado_id, 'Fechada')

            obter_fatura_status_vencimento(request.user, cartao_id, status, vencimento)
            
            # Filtra, dentre as faturas_abertas, se existe com a data de vencimento selecionada pelo usuário no formulário
            faturas_abertas = FaturaCartao.objects.filter(data_fatura=data_vencimento_cartao)
            qtd_fatura = len(faturas_abertas)

            
            print(f"Quantidade de faturas abertas do cartão {cartao}: {qtd_fatura}.") 
            print(f'Data Vencimento do cartão: {data_vencimento_cartao}.')
            print("Achou Fatura Aberta: ", faturas_abertas)

            hoje = datetime.now().date()

            # if FaturaCartao.objects.filter(cartao_selecionado=nova_despesa.cartao_selecionado_id): #, data_fatura=data_fechamento_cartao):
            #     print(">>>>>>>>>>>>>>>>>>>>>>> Achou a fatura!")
            # else:
            #     print(">>>>>>>>>>>>>>>>>>>>>>> Não achou a fatura!")

            # if hoje <= data_fechamento_cartao:
    


            #     print("Fatura do mês selecionado ABERTA! Quantidade de faturas abertas: ", qtd_fatura)
            # else:
            #     print("Fatura do mês selecionado FECHADA!")
            #     messages.error(request, 'A fatura selecionada encontra-se FECHADA. Reabra a Fatura caso necessário.')
            #     form = DespesaCartaoForms(request.user, instance=nova_despesa)
            #     return render(request, 'cartao/despesa-cartao-nova.html', {'form_nova_despesa': form})
            
            
            
            # print("Fatura: ---------------> ", qual_fatura)
            # print("Tipo: ---------------> ", type(qual_fatura))
            # print("Cartão: -------------", cartao)
            # print("Dia Vencimento Cartão: -------------", data_vencimento_cartao)
            # print("Tipo: ---------------> ", type(cartao.dia_vencimento_fatura))
            
            nova_despesa.data_registro -= timedelta(hours=4)
            nova_despesa.data_primeira_fatura = data_vencimento_cartao
            # dia_vencimento_cartao = cartao.dia_vencimento_fatura
            # dia_fechamento_cartao = cartao.dia_fechamento_fatura

            # print("Dia Vencimento: ---------------> ", dia_vencimento_cartao)
            # print("Dia Fechamento: ---------------> ", dia_fechamento_cartao)

            #dia_vencimento_fatura
            #dia_fechamento_fatura 
            # Apenas para teste. Apagar/Editar a linha abaixo. 
            #nova_despesa.data_primeira_fatura = datetime.now() - timedelta(hours=4)
            #print(nova_despesa.data_primeira_fatura)
            #nova_despesa.save()
            messages.success(request, 'Nova Despesa cadastradada com sucesso.')
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = DespesaCartaoForms(request.user)

    return render(request, 'cartao/despesa-cartao-nova.html', {'form_nova_despesa': form})

