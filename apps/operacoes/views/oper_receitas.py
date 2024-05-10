from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, date, datetime, timezone
from dateutil.relativedelta import relativedelta
from apps.configuracoes.models import Conta, CategoriaReceita
from apps.operacoes.models import Receita
from apps.operacoes.forms import ReceitaForms
from django.db.models import Case, Value, When, CharField
import locale

# Defina a localização para Português do Brasil (pt_BR)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# ----------------------------- Receitas ------------------------------------

def condicao_cores_receitas(lista):
   
    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores à lista com base na data usando annotate
    lista = lista.annotate(
        cor=Case(
            When(receita_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição à lista com base nas cores usando annotate
    lista = lista.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Creditada')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    print("Saiu da Lista")
    return lista

#ok
def receitas_todas(request):
    if not request.user.is_authenticated:
            messages.error(request, "Usuário não logado!")
            return redirect('login')
            
    if request.user.is_authenticated and request.user.is_superuser:
            receitas_cadastradas = Receita.objects.order_by("proprietario").all()
    else:
            receitas_cadastradas = Receita.objects.order_by("data", "-receita_status").filter(proprietario_id=request.user)
    
    # Define a data de hoje
    hoje = datetime.now().date()

    lista = condicao_cores_receitas(receitas_cadastradas)

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": lista, 'hoje': hoje})

#ok
def receitas_registradas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        receitas_registradas = Receita.objects.order_by("proprietario").filter(credito_ja_realizado='Não')
    
    else:
        receitas_registradas = Receita.objects.order_by("data").filter(proprietario_id=request.user, credito_ja_realizado='Não')     

    # Define a data de hoje
    hoje = datetime.now().date()

    lista = condicao_cores_receitas(receitas_registradas)

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": lista, 'hoje': hoje})

#ok
def receitas_efetivadas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        receitas_efetivadas = Receita.objects.order_by("proprietario").filter(credito_ja_realizado='Sim')
    
    else:
        receitas_efetivadas = Receita.objects.order_by("data").filter(proprietario_id=request.user, credito_ja_realizado='Sim')   
        
    # Define a data de hoje
    hoje = datetime.now().date()

    lista = condicao_cores_receitas(receitas_efetivadas)

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": lista, 'hoje': hoje})

#ok
def receitas_atrasadas(request):
    hoje=date.today()
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        receitas_atrasadas = Receita.objects.order_by("proprietario").filter(credito_ja_realizado='Não', data__lt=hoje)
    
    else:
        receitas_atrasadas = Receita.objects.order_by("data").filter(proprietario_id=request.user, credito_ja_realizado='Não', data__lt=hoje)     

    # Define a data de hoje
    hoje = datetime.now().date()

    lista = condicao_cores_receitas(receitas_atrasadas)

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": lista, 'hoje': hoje})

#ok
def receitas_futuras(request):
    hoje=date.today()
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        receitas_futuras = Receita.objects.order_by("proprietario").filter(credito_ja_realizado='Não', data__gte=hoje)
    
    else:
        receitas_futuras = Receita.objects.order_by("data").filter(proprietario_id=request.user, credito_ja_realizado='Não', data__gte=hoje)     
    
    # Define a data de hoje
    hoje = datetime.now().date()

    lista = condicao_cores_receitas(receitas_futuras)

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": lista, 'hoje': hoje})


def receitas_do_mes_atual(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_atual = datetime.now().month
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_atual), "%m").strftime("%B")

    if request.user.is_authenticated and request.user.is_superuser:
        receitas_do_mes = Receita.objects.order_by("proprietario").filter(data__month=mes_atual, data__year=hoje.year)
    else:
        receitas_do_mes = Receita.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_atual, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às receitas com base na data usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        cor=Case(
            When(receita_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às receitas com base nas cores usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": receitas_do_mes, 'hoje': nome_mes})

def receitas_do_mes_anterior(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_anterior = datetime.now().month - 1
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_anterior), "%m").strftime("%B")

    if request.user.is_authenticated and request.user.is_superuser:
        receitas_do_mes = Receita.objects.order_by("proprietario").filter(data__month=mes_anterior, data__year=hoje.year)
    else:
        receitas_do_mes = Receita.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_anterior, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às receitas com base na data usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        cor=Case(
            When(receita_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às receitas com base nas cores usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": receitas_do_mes, 'hoje': nome_mes})

def receitas_do_mes_proximo(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_proximo = datetime.now().month + 1
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_proximo), "%m").strftime("%B")


    if request.user.is_authenticated and request.user.is_superuser:
        receitas_do_mes = Receita.objects.order_by("proprietario").filter(data__month=mes_proximo, data__year=hoje.year)
    else:
        receitas_do_mes = Receita.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_proximo, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às receitas com base na data usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        cor=Case(
            When(receita_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às receitas com base nas cores usando annotate
    receitas_do_mes = receitas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/receita-index.html', {"lista_receitas": receitas_do_mes, 'hoje': nome_mes})

#ok
def nova_receita(request):
    print("Entrou em nova_receita............................................")
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_categorias_receitas = len(CategoriaReceita.objects.filter(proprietario=request.user))
    if quantidade_categorias_receitas == 0:
        messages.error(request, "Para registrar uma receita você precisa de uma Categoria de Receita!")
        return redirect('cadastrar-categoria-rec')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar uma receita você precisa de uma Conta para crédito da Receita!")
        return redirect('cadastrar-conta')

    if request.method == 'POST':
        print("Entrou em POST............................................")
        form = ReceitaForms(request.user, request.POST)
        if form.is_valid():
            print("Entrou em is_valid()............................................")
            nova_receita = form.save(commit=False)
            nova_receita.proprietario = request.user
            nova_receita.data_registro -= timedelta(hours=4)

            if ((nova_receita.credito_ja_realizado == 'Sim') and (nova_receita.data <= nova_receita.data_registro)):
                valor = nova_receita.valor
                conta_para_atualizar = Conta.objects.get(id=nova_receita.conta_credito_id)
                conta_para_atualizar.saldo += valor
                conta_para_atualizar.save()
            else:
                nova_receita.credito_ja_realizado = 'Não'

            nova_receita.save()
            messages.success(request, 'Nova receita cadastradada com sucesso.')
            return redirect('lista-receitas')
        else:
            print(form.errors)
    else:
        print("Entrou no else............................................")
        form = ReceitaForms(request.user)

    return render(request, 'operacoes/receita-nova.html', {'form_nova_receita': form})

#ok
def nova_receita_recorrente(request):
    print("Entrou em nova_receita_recorrente............................................")
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_categorias_receitas = len(CategoriaReceita.objects.filter(proprietario=request.user))
    if quantidade_categorias_receitas == 0:
        messages.error(request, "Para registrar uma receita você precisa de uma Categoria de Receita!")
        return redirect('cadastrar-categoria-rec')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar uma receita você precisa de uma Conta para crédito da Receita!")
        return redirect('cadastrar-conta')

    categorias = CategoriaReceita.objects.filter(proprietario=request.user)
    contas = Conta.objects.filter(proprietario=request.user)

    if request.method == 'POST':
        print("Entrou em POST............................................")
        
        repeticoes = int(request.POST.get('repeticoes', 2))
        periodicidade = request.POST.get('periodicidade', 'mensal')
        
        data_string = request.POST.get('data')

        # Converter a string em um objeto datetime
        nova_receita_data = datetime.strptime(data_string, "%Y-%m-%d")

        nova_receita_valor = request.POST.get('valor')
        nova_receita_credito_ja_realizado = 'Não'
        nova_receita_descricao = request.POST.get('descricao')

        categoria_id = request.POST.get('categoria')
        nova_receita_categoria = get_object_or_404(CategoriaReceita, id=categoria_id)
        
        conta_id = request.POST.get('conta_credito')
        print("Conta_ID do request: ", conta_id, " Tipo da variável conta_id: ", type(conta_id))
        nova_receita_conta = get_object_or_404(Conta, id=conta_id)

        nova_receita_receita_status = 'Registrado'
        nova_receita_data_registro = datetime.now() - timedelta(hours=4)
        nova_receita_proprietario = request.user

        print("-----------------------")
        print("Periodicidade: ", periodicidade)
        print("Repetições: ", repeticoes)

        for i in range(repeticoes):
            
            print("Parcela ", i+1, " R$ ", nova_receita_valor, " Data: ", nova_receita_data)

            # print("Data: ", nova_receita_data)
            # print("Valor: ", nova_receita_valor)
            # print("Crédito Realizado: ", nova_receita_credito_ja_realizado)
            # print("Descrição: ", nova_receita_descricao)
            # print("Categoria: ", nova_receita_categoria)
            # print("Conta: ", nova_receita_conta)
            # print("Status: ", nova_receita_receita_status)
            # print("Data do Registro: ", nova_receita_data_registro)
            # print("Proprietário: ", nova_receita_proprietario)

            nova_receita = Receita(
                data = nova_receita_data, 
                valor = nova_receita_valor,
                credito_ja_realizado = nova_receita_credito_ja_realizado,
                descricao = nova_receita_descricao,
                categoria = nova_receita_categoria,
                conta_credito = nova_receita_conta,
                receita_status = nova_receita_receita_status,
                data_registro = nova_receita_data_registro,              
                proprietario = nova_receita_proprietario
            )
            
            nova_receita.save()
            
            if periodicidade == 'Mensal':
                nova_receita_data += relativedelta(months=1)
            elif periodicidade == 'Semanal':
                nova_receita_data += relativedelta(weeks=1)
            else:
                nova_receita_data += relativedelta(years=1)

        messages.success(request, f'{repeticoes} nova(s) receita(s) recorrente(s) cadastrada(s) com sucesso.')
        return redirect('lista-receitas')
    
    else:
        contexto = {
            'categorias': categorias,
            'contas': contas,
        }
        return render(request, 'operacoes/receita-nova-recorrente.html', contexto)

#ok
def efetivar_receita(request, receita_id):
    # Obtém a instância da Receita a ser editada
    receita_para_efetivar = get_object_or_404(Receita, id=receita_id)

    # Verifica se o usuário logado é o proprietário da Receita
    if receita_para_efetivar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Receitas de outros usuários.')
        return redirect('lista-receitas')
    
    # Verifica se o status da Receita é "Registrado"
    if receita_para_efetivar.receita_status == 'Efetivado':
        messages.error(request, 'Não é possível efetivar uma Receita já efetivada.')
        return redirect('lista-receitas')   
    
    if (datetime.now(timezone.utc) >= receita_para_efetivar.data):
        receita_para_efetivar.credito_ja_realizado = 'Sim'
        receita_para_efetivar.receita_status = 'Efetivado'

        valor = receita_para_efetivar.valor

        conta_para_atualizar = Conta.objects.get(id=receita_para_efetivar.conta_credito_id)
        conta_para_atualizar.saldo += valor #credita na conta escolhida
        
        conta_para_atualizar.save()          
        receita_para_efetivar.save()

        messages.success(request, f'Receita Efetivado com sucesso.')

        return redirect('lista-receitas-efetivadas')
    
    else:
        messages.error(request, 'Não é possível Efetivar uma Receita com data futura. Sua Receita continua com o status de "Registrado".')       
        return redirect('lista-receitas')

#ok
def devolver_receita(request, receita_id):
    # Obtém a instância da Receita a ser editada
    receita_para_devolver = get_object_or_404(Receita, id=receita_id)

    # Verifica se o usuário logado é o proprietário da Receita
    if receita_para_devolver.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Receitas de outros usuários.')
        return redirect('lista-receitas')
    
    # Verifica se o status da Receita é "Registrado"
    if receita_para_devolver.receita_status == 'Registrado':
        messages.error(request, 'Não é possível Devolver uma Receita "Não Efetivada".')
        return redirect('lista-receitas')

    receita_para_devolver = Receita.objects.get(id=receita_id)    
    receita_para_devolver.credito_ja_realizado = 'Não'
    receita_para_devolver.receita_status = 'Registrado'

    valor = receita_para_devolver.valor

    conta_para_atualizar = Conta.objects.get(id=receita_para_devolver.conta_credito_id)
    conta_para_atualizar.saldo -= valor #debita da conta escolhida
    
    conta_para_atualizar.save()          
    receita_para_devolver.save()

    messages.success(request, f'Receita Devolvida com sucesso. Status: "Registrado".')
    return redirect('lista-receitas')

#ok
def editar_receita(request, receita_id): # Premissa: receita não efetivada, ou seja, receita registrada!
    # Obtém a instância da Receita a ser editada
    receita_para_editar = get_object_or_404(Receita, id=receita_id)

    # Verifica se o usuário logado é o proprietário da Receita
    if receita_para_editar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Receitas de outros usuários.')
        return redirect('lista-receitas')
    
    # Verifica se o status da Receita é "Registrado"
    if receita_para_editar.receita_status != 'Registrado':
        messages.error(request, 'Não é possível editar uma Receita efetivada.')
        return redirect('lista-receitas')
    
    form = ReceitaForms(request.user, instance=receita_para_editar)

    if request.method == 'POST':
        form = ReceitaForms(request.user, request.POST, instance=receita_para_editar)
        if form.is_valid():
            form.save()   
            messages.success(request, 'Receita editada com sucesso.')
            return redirect('lista-receitas')
    return render(request, 'operacoes/receita-editar.html', {'form_editar_receita': form, 'receita_id': receita_id})

#ok
def deletar_receita(request, receita_id): #falta criar uma logica para confirmar se realmente quer deletar a receita

    # Obtém a instância da Receita a ser deletada
    receita_para_deletar = get_object_or_404(Receita, id=receita_id)

    # Verifica se o usuário logado é o proprietário da Receita
    if receita_para_deletar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Receitas de outros usuários.')
        return redirect('lista-receitas')

    if receita_para_deletar.credito_ja_realizado == 'Sim':
        conta_para_atualizar = Conta.objects.get(id=receita_para_deletar.conta_credito_id)
        conta_para_atualizar.saldo -= receita_para_deletar.valor
        conta_para_atualizar.save()
        messages.success(request, f'Receita deletada com sucesso e o saldo da conta "{conta_para_atualizar.descricao}" foi atualizado.')

    else:
        # Se não houver atualização de saldo, exibe apenas a mensagem de deleção
        messages.success(request, 'Receita deletada com sucesso.')
    
    receita_para_deletar.delete()
    return redirect('lista-receitas')

def receita_detalhada(request, receita_id):
    # Obtém a instância da Receita a ser editada
    receita_para_detalhar = get_object_or_404(Receita, id=receita_id)
    
    # Verifica se o usuário logado é o proprietário da Receita
    if receita_para_detalhar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Receitas de outros usuários.')
        return redirect('lista-receitas')
   
    #form = receitaForms(request.user, instance=receita_para_detalhar)
    
    hoje = datetime.now().replace(hour=0, minute=0, second=1, microsecond=999999).date()
    data_da_receita = receita_para_detalhar.data.replace(hour=23, minute=59, second=59, microsecond=999999).date()
    

    # print(">>>>>>>>>>>>>>>>>>>>>>>>", hoje)
    # print("------------------------", data_da_despesa)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    if receita_para_detalhar.receita_status == 'Registrado': 
        #if (despesa_para_detalhar.data.replace(tzinfo=None) < hoje):
        if (data_da_receita < hoje):
            condicao = 'Atrasada'
            cor = vermelho
        elif (data_da_receita == hoje):
            condicao = 'Hoje'
            cor = amarelo
        else:
            condicao = 'Futura'
            cor = azul
    else:
        condicao = 'Paga'
        cor = verde
    
    print("------------------------", condicao)

    return render(request, 'operacoes/receita-detalhada.html', {'receita': receita_para_detalhar, 'condicao': condicao, 'cor': cor})