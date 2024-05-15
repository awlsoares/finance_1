from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from apps.configuracoes.models import Conta
from apps.operacoes.models import Receita, Despesa, InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada
from apps.configuracoes.forms import ContaForms, CategoriaDespesa
from datetime import timedelta, datetime, date
from decimal import Decimal
import pandas as pd
import sqlite3

def index(request):
        if not request.user.is_authenticated:
                #messages.error(request, "Usuário não logado!")
                
                mensagem_tipo = "erro"
                mensagem_conteudo = "Usuário não logado!"
                return redirect('login')
                #return render(request, 'usuarios/login.html', {"mensagem_tipo": mensagem_tipo, "mensagem_conteudo": mensagem_conteudo})
        
        
        receitas, despesas, consumo = balanço_anual_e_velocimetro(request)
        
        legenda_piramide, valores_piramide = piramide(request)
        
        atrasadas = contar_todas_as_despesas_atrasadas(request)

        a_vencer = contar_despesas_a_vencer_no_mes_atual(request)

        contexto = {
             "receitas": receitas,
             "despesas": despesas,
             "consumo_receita": consumo,
             "cat_despesas": legenda_piramide,
             "gastos_por_categoria": valores_piramide,
             "numero_despesas_atrasadas": atrasadas,
             "numero_despesas_a_vencer_no_mes_atual": a_vencer,
        }

        print(legenda_piramide)
        print(valores_piramide)

        return render(request, 'base/index_base.html', contexto)


def consultar_tabela_sql(nome_da_tabela):
     
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('db.sqlite3')  # Substitua 'arquivo.db' pelo nome do seu arquivo SQLite

    # Definir a consulta SQL para selecionar os dados da tabela desejada
    consulta_sql = f"SELECT * FROM {nome_da_tabela}"  # Substitua 'nome_da_tabela' pelo nome da tabela desejada

    # Carregar os dados da tabela em um DataFrame
    df = pd.read_sql_query(consulta_sql, conn)

    # Fechar a conexão com o banco de dados
    conn.close()

    # Exibir as primeiras linhas do DataFrame para verificar se os dados foram carregados corretamente
    #print(df.head())

    return df

def balanço_anual_e_velocimetro(request):

    # Obter a data atual
    data_atual = datetime.now()

    # Extrair o número do mês
    numero_mes = data_atual.month

    ano_escolhido = 2024
    valor_receitas_mensal = []
    valor_despesas_mensal = []
    
    for i in range(1, 13):
            valor_receitas_mensal.append(obter_valor_receitas_mensal(request, i, ano_escolhido))
            valor_despesas_mensal.append(-obter_valor_despesas_mensal(request, i, ano_escolhido))

    receita_mes_atual = valor_receitas_mensal[numero_mes - 1]
    despesa_mes_atual = valor_despesas_mensal[numero_mes - 1]
    consumo_da_receita = 100 * (- (despesa_mes_atual / receita_mes_atual))
    consumo_da_receita = [consumo_da_receita]
    
    #print(consumo_da_receita)

    return valor_receitas_mensal, valor_despesas_mensal, consumo_da_receita

def piramide(request):
     
    despesas_por_categoria = obter_despesas_por_categoria(request, 2024)
    # Salvar as chaves do dicionário em uma lista
    chaves_do_dicionario = list(despesas_por_categoria.keys())

    df = consultar_tabela_sql('configuracoes_categoriadespesa')
    #print(df)
    # Mapeando os IDs para suas respectivas descrições
    descricoes_chaves = df[df['id'].isin(chaves_do_dicionario)]['descricao'].tolist()

    #print(descricoes_chaves)

    chaves_do_dicionario = [str(numero) for numero in chaves_do_dicionario]
    #print(chaves_do_dicionario)
    
    # Extrair os valores do dicionário e converter em lista
    valores_lista = list(despesas_por_categoria.values())
    #print(valores_lista)

    return descricoes_chaves, valores_lista

def obter_valor_receitas_mensal(request, mes, ano):
    # Filtra as receitas para o mês e ano desejados
    receitas_do_mes = Receita.objects.filter(proprietario=request.user, data__month=mes, data__year=ano)
    
    # Calcula a soma dos valores das receitas do mês
    total_receitas_mes = receitas_do_mes.aggregate(soma_receitas=Sum('valor'))['soma_receitas']
    
    # Verifica se a soma é None (nenhuma receita encontrada)
    if total_receitas_mes is None:
        total_receitas_mes = 0
    else:
        # Converte o valor Decimal para float com duas casas decimais
        total_receitas_mes = float(total_receitas_mes.quantize(Decimal('.01')))
    
    return total_receitas_mes

def obter_valor_despesas_mensal(request, mes, ano):
    # Filtra as despesas para o mês e ano desejados
    despesas_do_mes = Despesa.objects.filter(proprietario=request.user, data__month=mes, data__year=ano)
    
    # Calcula a soma dos valores das despesas do mês
    total_despesas_mes = despesas_do_mes.aggregate(soma_despesas=Sum('valor'))['soma_despesas']
    
    # Verifica se a soma é None (nenhuma despesa encontrada)
    if total_despesas_mes is None:
        total_despesas_mes = 0
    else:
        # Converte o valor Decimal para float com duas casas decimais
        total_despesas_mes = float(total_despesas_mes.quantize(Decimal('.01')))
    
    return total_despesas_mes

def contar_todas_as_despesas_atrasadas(request):

    hoje=date.today()
               
    if request.user.is_authenticated and request.user.is_superuser:
        despesas_atrasadas = len(Despesa.objects.filter(debito_ja_realizado='Não', data__lt=hoje))
    
    else:
        despesas_atrasadas = len(Despesa.objects.filter(proprietario_id=request.user, debito_ja_realizado='Não', data__lt=hoje))
    
    return despesas_atrasadas

def contar_despesas_a_vencer_no_mes_atual(request):
     
    hoje=date.today()

    if request.user.is_authenticated and request.user.is_superuser:
        despesas_atrasadas = len(Despesa.objects.filter(debito_ja_realizado='Não', data__month=hoje.month, data__year=hoje.year, data__lt=hoje))
        despesas_a_vencer = len(Despesa.objects.filter(debito_ja_realizado='Não', data__month=hoje.month, data__year=hoje.year)) - despesas_atrasadas

    else:
        despesas_atrasadas = len(Despesa.objects.filter(proprietario_id=request.user, debito_ja_realizado='Não', data__month=hoje.month, data__year=hoje.year, data__lt=hoje))
        despesas_a_vencer = len(Despesa.objects.filter(proprietario_id=request.user, debito_ja_realizado='Não', data__month=hoje.month, data__year=hoje.year)) - despesas_atrasadas

    return despesas_a_vencer

def obter_despesas_por_categoria(request, ano):

    df_despesas = consultar_tabela_sql('operacoes_despesa')
    despesas_por_categoria = df_despesas.groupby('categoria_id')['valor'].sum()
    print(df_despesas)
    print(despesas_por_categoria)

    # Converter a coluna 'data' para o tipo datetime
    df_despesas['data'] = pd.to_datetime(df_despesas['data'])

    # Criar um dicionário para armazenar os totais de gastos por categoria e mês
    total_gastos_por_categoria = {}

    # Iterar sobre cada categoria
    for categoria_id, grupo_categoria in df_despesas.groupby('categoria_id'):
        # Inicializar a lista de gastos para esta categoria
        gastos_por_mes = [0.0] * 12
        
        # Iterar sobre cada mês de janeiro a dezembro de 2024
        for mes in range(1, 13):
            # Filtrar as despesas da categoria para o mês atual
            despesas_do_mes = grupo_categoria[grupo_categoria['data'].dt.month == mes]
            # Calcular o total de gastos para o mês atual
            total_gasto = despesas_do_mes['valor'].sum()
            # Armazenar o total de gastos para o mês atual na lista
            gastos_por_mes[mes - 1] = total_gasto
            
        # Adicionar a lista de gastos por mês no dicionário, com a categoria_id como chave
        total_gastos_por_categoria[categoria_id] = gastos_por_mes

    # Exibir o dicionário resultante
    print(total_gastos_por_categoria)
    print("tamanho: ", len(total_gastos_por_categoria))

    # Salvar as chaves do dicionário em uma lista
    chaves_do_dicionario = list(total_gastos_por_categoria.keys())
    print(chaves_do_dicionario)

    # # Extrair os valores do dicionário e converter em lista
    # valores_lista = list(despesas_por_categoria.values())
    # print(valores_lista)

    return total_gastos_por_categoria
