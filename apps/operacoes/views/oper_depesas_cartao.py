from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, date, datetime, timezone
from dateutil.relativedelta import relativedelta
from apps.configuracoes.models import Conta, CategoriaDespesa, CartaoCredito
from apps.operacoes.models import DespesaCartao, DespesaIndividualizadaCartao, FaturaCartao
from apps.operacoes.forms import DespesaForms, DespesaCartaoForms
from django.db.models import Case, Value, When, CharField

# ---------------------- Despesas Cartão de Crédito --------------------------

# Verifica e obtem as faturas por status
def obter_faturas_status(usuario, cartao_id, status):
    return FaturaCartao.objects.filter(proprietario=usuario, cartao_selecionado=cartao_id, fatura_status=status)

# Verifica e obtem as despesas individualizadas por fatura
def obter_desp_ind_por_fatura(usuario, cartao_id, fatura):
    return DespesaIndividualizadaCartao.objects.filter(proprietario=usuario, qual_cartao=cartao_id, qual_fatura=fatura)

# Realizar o registro de uma nova fatura do cartão com status 'Aberta'.
def registrar_fatura(usuario, cartao, dia, mes, ano):
    data_vencimento = str(ano) + '-' + str(mes) + '-' + str(dia) 
    data_vencimento = (datetime.strptime(data_vencimento, '%Y-%m-%d')).date()
    
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
    #print(f'Usuário: {usuario}. Cartão: {cartao}. Data Vencimento: {data_vencimento}.')

# Gerar e salvas as parcelas do cartão como despesas individualizadas.
def gerar_despesa_individualizada_cartao(request, despesa):
    # print("----------------------------------------------")
    # print("Data: ", despesa.data, " Tipo: ", type(despesa.data))
    # print("Valor: ", despesa.valor, " Tipo: ", type(despesa.valor))
    # print("Qual Parcela: 1")
    # print("Total Parcelas: ", despesa.numero_parcelas, " Tipo: ", type(despesa.numero_parcelas))
    # print("Descrição: ", despesa.descricao, " Tipo: ", type(despesa.descricao))
    # print("Categoria: ", despesa.categoria, " Tipo: ", type(despesa.categoria))
    # print("Despesa Associada: ", despesa.id, " Tipo: ", type(despesa.id))
    # print("Qual Cartão: ", despesa.cartao_selecionado, " Tipo: ", type(despesa.cartao_selecionado))
    # print("Despesa Status: Registrada.")
    # print("Data Registro: ", datetime.now())
    # print("Proprietário: ", despesa.proprietario, " Tipo: ", type(despesa.proprietario))
    # print("Qual Fatura: ", despesa.data_primeira_fatura, " Tipo: ", type(despesa.data_primeira_fatura))

    fatura_escolhida = despesa.data_primeira_fatura    
    qtd_total_parcelas = despesa.numero_parcelas
    valor_parcela = (despesa.valor) / qtd_total_parcelas
    parcela = 1
    while parcela <= qtd_total_parcelas:

        nova_despesa = DespesaIndividualizadaCartao(
            data = despesa.data,
            valor = valor_parcela,
            qual_parcela = parcela,
            total_parcelas = despesa.numero_parcelas,
            descricao = despesa.descricao,
            categoria = despesa.categoria,
            despesa_associada = despesa,
            qual_cartao = despesa.cartao_selecionado,
            despesa_status = 'Registrada',
            data_registro = datetime.now(),              
            proprietario = despesa.proprietario,
            qual_fatura = fatura_escolhida
        )
        parcela += 1 

        # Obtenha o próximo mês
        if fatura_escolhida.month == 12:
            fatura_escolhida = fatura_escolhida.replace(year=fatura_escolhida.year + 1, month=1)
        else:
            fatura_escolhida = fatura_escolhida.replace(month=fatura_escolhida.month + 1)
            
        # print("-------------------------------")
        # print(nova_despesa.qual_fatura)
        # print(nova_despesa.valor)
        nova_despesa.save()
        messages.success(request, f'Despesa Cadastrada com sucesso.')

# Seleciona o cartão e a fatura para registrar a despesa
def nova_despesa_cartao(request):

    cartoes = CartaoCredito.objects.filter(proprietario=request.user)

    # Itera em todos os cartões do usuário e se não houver fatura aberta providencia o registro de uma nova fatura
    for cartao in cartoes:
        quantidade = len(obter_faturas_status(request.user, cartao.id, 'Aberta'))
        if quantidade != 0:
            print(f'O cartão {cartao.descricao} TEM {quantidade} Fatura(s) Aberta(s).')
        else:
            print(f'O cartão {cartao.descricao} NÃO TEM Fatura Aberta.')
            cartao = CartaoCredito.objects.get(pk=cartao.id)
            dia_vencimento = cartao.dia_vencimento_fatura
            dia_fechamento = cartao.dia_fechamento_fatura
            hoje = datetime.now().date()
            
            if dia_vencimento > dia_fechamento: # fatura vence no mesmo mês de fechamento
                if hoje.day < dia_fechamento:
                    mes = hoje.month
                    ano = hoje.year
                else:
                    if hoje.month != 12:
                        mes = hoje.month + 1
                        ano = hoje.year
                    else:
                        mes = 1
                        ano = hoje.year + 1

            else: # dia_vencimento < dia_fechamento. Exemplo: Fecha dia 26 e vence no dia 10 do mes seguinte
                if hoje.day < dia_fechamento:
                    if hoje.month != 12:
                        mes = hoje.month + 1
                        ano = hoje.year
                    else:     
                        mes = 1
                        ano = hoje.year + 1
                else:
                    if hoje.mes <= 10:
                        mes = hoje.month + 2
                        ano = hoje.year
                    else:
                        if hoje.mes == 11:
                            mes = 1
                            ano = hoje.year + 1
                        else:
                            mes = 2
                            ano = hoje.year + 1

            registrar_fatura(request.user, cartao, dia_vencimento, mes, ano)

    faturas = FaturaCartao.objects.filter(proprietario=request.user, fatura_status='Aberta')

    if request.method == 'POST':
        
        despesa_data_debito = request.POST.get('data_debito')
        despesa_data_debito = datetime.strptime(despesa_data_debito, "%Y-%m-%d")
        
        despesa_valor = request.POST.get('valor')
        despesa_descricao = request.POST.get('descricao')
        categoria_id = request.POST.get('categoria')
        despesa_categoria = get_object_or_404(CategoriaDespesa, id=categoria_id)
        
        cartao_id = request.POST.get('cartao')
        despesa_cartao_escolhido = get_object_or_404(CartaoCredito, id=cartao_id)
    
        fatura_selecionada_id = request.POST.get('opcao')
        despesa_fatura_selecionada = get_object_or_404(FaturaCartao, id=fatura_selecionada_id)

        despesa_qtd_parcelas = int(request.POST.get('qtd_parcelas'))
        
        # print("Data do Débito: ", despesa_data_debito, " Tipo: ", type(despesa_data_debito))
        # print("Valor R$ ", despesa_valor, " Tipo: ", type(despesa_valor))
        # print("Descrição: ", despesa_descricao, " Tipo: ", type(despesa_descricao))
        # print("Categoria da Despesa: ", despesa_categoria, " Tipo: ", type(despesa_categoria))
        # print("Cartão escolhido: ", despesa_cartao_escolhido, " Tipo: ", type(despesa_cartao_escolhido))
        # print("Fatura selecionada: ", despesa_fatura_selecionada, " Tipo: ", type(despesa_fatura_selecionada))
        # print("Número de Parcelas: ", despesa_qtd_parcelas, " Tipo: ", type(despesa_qtd_parcelas))

        nova_despesa = DespesaCartao(
                data = despesa_data_debito, 
                valor = despesa_valor,
                numero_parcelas = despesa_qtd_parcelas,
                descricao = despesa_descricao,
                categoria = despesa_categoria,
                cartao_selecionado = despesa_cartao_escolhido,
                despesa_status = 'Registrada',
                data_registro = datetime.now(),              
                proprietario = request.user,
                data_primeira_fatura = despesa_fatura_selecionada.data_fatura
            )
        
        nova_despesa.save()

        nova_despesa = get_object_or_404(DespesaCartao, id=(DespesaCartao.objects.latest('id').id))

        gerar_despesa_individualizada_cartao(request, nova_despesa)
        
        return redirect('index')

    contexto = {
        'cartoes': cartoes,
        'faturas': faturas,
        'categorias': CategoriaDespesa.objects.filter(proprietario=request.user)
    }
    return render(request, 'cartao/cartao-despesa-nova.html', contexto)

# Gerar extrato parcial de fatura do cartão
def gerar_fatura_parcial(request):

    # Define a data de hoje
    hoje = datetime.now().date()

    if request.method == 'POST':
        
        cartao_id = request.POST.get('cartao')
        despesa_cartao_escolhido = get_object_or_404(CartaoCredito, id=cartao_id)  
        fatura_selecionada_id = request.POST.get('opcao')
        despesa_fatura_selecionada = get_object_or_404(FaturaCartao, id=int(fatura_selecionada_id))

        if (despesa_fatura_selecionada.data_fatura != 'None') and (cartao_id != 'None'):

            despesas_cadastradas = DespesaIndividualizadaCartao.objects.filter(
                proprietario_id=request.user.id,
                qual_fatura=despesa_fatura_selecionada.data_fatura,
                qual_cartao=cartao_id)
            
        elif (despesa_fatura_selecionada.data_fatura == 'None') and (cartao_id != 'None'):
            despesas_cadastradas = DespesaIndividualizadaCartao.objects.filter(
                proprietario_id=request.user.id,
                qual_cartao=cartao_id)
            
        else:
            despesas_cadastradas = DespesaIndividualizadaCartao.objects.filter(
                proprietario_id=request.user.id,
                qual_fatura=despesa_fatura_selecionada.data_fatura)
        
        
        print("cartao_id: ", cartao_id)
        print("despesa_cartao_escolhido: ", despesa_cartao_escolhido)
        print("fatura_selecionada_id: ", fatura_selecionada_id)
        print("despesa_fatura_selecionada: ", despesa_fatura_selecionada)
        print("despesas_cadastradas: ", despesas_cadastradas)
        
        cartoes = CartaoCredito.objects.filter(proprietario=request.user)
        faturas = FaturaCartao.objects.filter(proprietario=request.user)




    else:
        despesas_cadastradas = DespesaIndividualizadaCartao.objects.filter(proprietario_id=request.user.id)
        cartoes = CartaoCredito.objects.filter(proprietario=request.user)
        faturas = FaturaCartao.objects.filter(proprietario=request.user)
        
    contexto = {
        'lista_despesas': despesas_cadastradas,
        'hoje': hoje,
        'cartoes': cartoes,
        'faturas': faturas
    }

    return render(request, 'cartao/despesa-cartao-index.html', contexto)


def fatura_parcial_cartao(request):

    # Define a data de hoje
    hoje = datetime.now().date()


    despesas_fatura = obter_desp_ind_por_fatura(request.user, 4, '2024-03-25') # Especifica 25/03/2024. Ajustar para qualquer fatura

    #despesas_cadastradas = DespesaIndividualizadaCartao.objects.filter(proprietario_id=request.user.id)
    
    return render(request, 'cartao/despesa-cartao-index.html', {"lista_despesas": despesas_fatura, 'hoje': hoje})

def filtrar_despesas_individualizadas_cartao(request):
    opcoes_cartoes = CartaoCredito(proprietario_id=request.user.id)