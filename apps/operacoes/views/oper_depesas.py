from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, date, datetime, timezone
from dateutil.relativedelta import relativedelta
from apps.configuracoes.models import Conta, CategoriaDespesa
from apps.operacoes.models import Despesa
from apps.operacoes.forms import DespesaForms
from django.db.models import Case, Value, When, CharField
import locale

# Defina a localização para Português do Brasil (pt_BR)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# ----------------------------- Despesas ------------------------------------

#ok
def despesa_nova(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_categorias_despesas = len(CategoriaDespesa.objects.filter(proprietario=request.user))
    if quantidade_categorias_despesas == 0:
        messages.error(request, "Para registrar uma despesa você precisa de uma Categoria de Despesa!")
        return redirect('cadastrar-categoria-desp')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar uma despesa você precisa de uma Conta para débito da Despesa!")
        return redirect('cadastrar-conta')

    if request.method == 'POST':
        form = DespesaForms(request.user, request.POST)
        if form.is_valid():
            nova_despesa = form.save(commit=False)
            nova_despesa.proprietario = request.user
            nova_despesa.data_registro -= timedelta(hours=4)

            if ((nova_despesa.debito_ja_realizado == 'Sim') and (nova_despesa.data <= nova_despesa.data_registro)):
                valor = nova_despesa.valor
                conta_para_atualizar = Conta.objects.get(id=nova_despesa.conta_debito_id)
                conta_para_atualizar.saldo -= valor
                conta_para_atualizar.save()
                nova_despesa.despesa_status = 'Efetivado'
            else:
                nova_despesa.debito_ja_realizado = 'Não'

            nova_despesa.save()
            messages.success(request, 'Nova Despesa cadastradada com sucesso.')
            return redirect('lista-despesas')
        else:
            print(form.errors)
    else:
        form = DespesaForms(request.user)

    return render(request, 'operacoes/despesa-nova.html', {'form_nova_despesa': form})

#ok
def nova_despesa_recorrente(request):
    print("Entrou em nova_despesa_recorrente............................................")
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_categorias_despesas = len(CategoriaDespesa.objects.filter(proprietario=request.user))
    if quantidade_categorias_despesas == 0:
        messages.error(request, "Para registrar uma despesa você precisa de uma Categoria de Despesa!")
        return redirect('cadastrar-categoria-desp')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar uma despesa você precisa de uma Conta para débito da Despesa!")
        return redirect('cadastrar-conta')

    categorias = CategoriaDespesa.objects.filter(proprietario=request.user)
    contas = Conta.objects.filter(proprietario=request.user)

    if request.method == 'POST':
        print("Entrou em POST............................................")
        
        repeticoes = int(request.POST.get('repeticoes', 2))
        periodicidade = request.POST.get('periodicidade', 'Mensal')
        
        data_string = request.POST.get('data')

        # Converter a string em um objeto datetime
        nova_despesa_data = datetime.strptime(data_string, "%Y-%m-%d")

        nova_despesa_valor = request.POST.get('valor')
        nova_despesa_debito_ja_realizado = 'Não'
        nova_despesa_descricao = request.POST.get('descricao')

        categoria_id = request.POST.get('categoria')
        nova_despesa_categoria = get_object_or_404(CategoriaDespesa, id=categoria_id)
        
        conta_id = request.POST.get('conta_debito')
        nova_despesa_conta = get_object_or_404(Conta, id=conta_id)

        nova_despesa_despesa_status = 'Registrado'
        nova_despesa_data_registro = datetime.now() - timedelta(hours=4)
        nova_despesa_proprietario = request.user

        print("-----------------------")
        print("Periodicidade: ", periodicidade)
        print("Repetições: ", repeticoes)

        for i in range(repeticoes):
            
            print("Parcela ", i+1, " R$ ", nova_despesa_valor, " Data: ", nova_despesa_data)
            print("Data: ", nova_despesa_data)
            print("Valor: ", nova_despesa_valor)
            print("Débito Realizado: ", nova_despesa_debito_ja_realizado)
            print("Descrição: ", nova_despesa_descricao)
            print("Categoria: ", nova_despesa_categoria)
            print("Conta: ", nova_despesa_conta)
            print("Status: ", nova_despesa_despesa_status)
            print("Data do Registro: ", nova_despesa_data_registro)
            print("Proprietário: ", nova_despesa_proprietario)

            nova_despesa = Despesa(
                data = nova_despesa_data, 
                valor = nova_despesa_valor,
                debito_ja_realizado = nova_despesa_debito_ja_realizado,
                descricao = nova_despesa_descricao,
                categoria = nova_despesa_categoria,
                conta_debito = nova_despesa_conta,
                despesa_status = nova_despesa_despesa_status,
                data_registro = nova_despesa_data_registro,              
                proprietario = nova_despesa_proprietario
            )
            
            nova_despesa.save()
            
            if periodicidade == 'Mensal':
                nova_despesa_data += relativedelta(months=1)
            elif periodicidade == 'Semanal':
                nova_despesa_data += relativedelta(weeks=1)
            else:
                nova_despesa_data += relativedelta(years=1)

        messages.success(request, f'{repeticoes} nova(s) despesa(s) recorrente(s) cadastrada(s) com sucesso.')
        return redirect('lista-despesas')
    
    else:
        contexto = {
            'categorias': categorias,
            'contas': contas,
        }
        return render(request, 'operacoes/despesa-nova-recorrente.html', contexto)

#ok
def despesas_todas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    # Verifica se o usuário é superusuário
    if request.user.is_superuser:
        despesas_cadastradas = Despesa.objects.order_by("proprietario").all()
    else:
        # Filtra as despesas do usuário logado e ordena por status e data
        despesas_cadastradas = Despesa.objects.order_by("data", "-despesa_status").filter(proprietario=request.user)
    
    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_cadastradas = despesas_cadastradas.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_cadastradas = despesas_cadastradas.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )
    
    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_cadastradas, 'hoje': hoje})

#ok
def despesas_registradas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        despesas_registradas = Despesa.objects.order_by("proprietario").filter(debito_ja_realizado='Não')
    
    else:
        despesas_registradas = Despesa.objects.order_by("data").filter(proprietario_id=request.user, debito_ja_realizado='Não')
    
    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_registradas = despesas_registradas.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_registradas = despesas_registradas.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )
         
    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_registradas})

#ok
def despesas_efetivadas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        despesas_efetivadas = Despesa.objects.order_by("proprietario").filter(debito_ja_realizado='Sim')
    
    else:
        despesas_efetivadas = Despesa.objects.order_by("data").filter(proprietario_id=request.user, debito_ja_realizado='Sim')     
    
    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_efetivadas = despesas_efetivadas.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_efetivadas = despesas_efetivadas.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_efetivadas})

#ok
def despesas_atrasadas(request):
    hoje=date.today()
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        despesas_atrasadas = Despesa.objects.order_by("proprietario").filter(debito_ja_realizado='Não', data__lt=hoje)
    
    else:
        despesas_atrasadas = Despesa.objects.order_by("data").filter(proprietario_id=request.user, debito_ja_realizado='Não', data__lt=hoje)  

    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_atrasadas = despesas_atrasadas.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_atrasadas = despesas_atrasadas.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_atrasadas})

#ok
def despesas_futuras(request):
    hoje=date.today()
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
               
    if request.user.is_authenticated and request.user.is_superuser:
        despesas_futuras = Despesa.objects.order_by("proprietario").filter(debito_ja_realizado='Não', data__gte=hoje)
    
    else:
        despesas_futuras = Despesa.objects.order_by("data").filter(proprietario_id=request.user, debito_ja_realizado='Não', data__gte=hoje)    

    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_futuras = despesas_futuras.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_futuras = despesas_futuras.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_futuras})

def despesas_do_mes_atual(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_atual = datetime.now().month
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_atual), "%m").strftime("%B")

    if request.user.is_authenticated and request.user.is_superuser:
        despesas_do_mes = Despesa.objects.order_by("proprietario").filter(data__month=mes_atual, data__year=hoje.year)
    else:
        despesas_do_mes = Despesa.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_atual, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_do_mes, 'hoje': nome_mes})

def despesas_do_mes_anterior(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_anterior = datetime.now().month - 1
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_anterior), "%m").strftime("%B")

    if request.user.is_authenticated and request.user.is_superuser:
        despesas_do_mes = Despesa.objects.order_by("proprietario").filter(data__month=mes_anterior, data__year=hoje.year)
    else:
        despesas_do_mes = Despesa.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_anterior, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_do_mes, 'hoje': nome_mes})

def despesas_do_mes_proximo(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    mes_proximo = datetime.now().month + 1
    hoje = datetime.now().date()
    nome_mes = datetime.strptime(str(mes_proximo), "%m").strftime("%B")


    if request.user.is_authenticated and request.user.is_superuser:
        despesas_do_mes = Despesa.objects.order_by("proprietario").filter(data__month=mes_proximo, data__year=hoje.year)
    else:
        despesas_do_mes = Despesa.objects.order_by("data").filter(proprietario_id=request.user, data__month=mes_proximo, data__year=hoje.year)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        cor=Case(
            When(despesa_status='Efetivado', then=Value(verde)),
            When(data__lt=hoje, then=Value(vermelho)),
            When(data=hoje, then=Value(amarelo)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    # Atribui condição às despesas com base nas cores usando annotate
    despesas_do_mes = despesas_do_mes.annotate(
        condicao=Case(
            When(cor=verde, then=Value('Paga')),
            When(cor=vermelho, then=Value('Atrasada')),
            When(cor=amarelo, then=Value('Hoje')),
            default=Value('Futura'),
            output_field=CharField(),
        )
    )

    return render(request, 'operacoes/despesa-index.html', {"lista_despesas": despesas_do_mes, 'hoje': nome_mes})
#ok
def despesas_efetivar(request, despesa_id):
    # Obtém a instância da Despesa a ser editada
    despesa_para_efetivar = get_object_or_404(Despesa, id=despesa_id)

    # Verifica se o usuário logado é o proprietário da Despesa
    if despesa_para_efetivar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-despesas')
    
    # Verifica se o status da Despesa é "Registrado"
    if despesa_para_efetivar.despesa_status == 'Efetivado':
        messages.error(request, 'Não é possível efetivar uma Despesa já efetivada.')
        return redirect('lista-despesas')
    
    # Verifica se a data da Despesa é uma Data Futura.
    if datetime.now(timezone.utc) < despesa_para_efetivar.data:
        messages.error(request, 'Não é possível Efetivar uma Despesa com data futura. Sua Despesa continua com o status de "Registrado".')       
        return redirect('lista-despesas')
        
    despesa_para_efetivar.debito_ja_realizado = 'Sim'
    despesa_para_efetivar.despesa_status = 'Efetivado'

    conta_para_atualizar = Conta.objects.get(id=despesa_para_efetivar.conta_debito_id)
    conta_para_atualizar.saldo -= despesa_para_efetivar.valor # Debita da conta escolhida
    
    conta_para_atualizar.save()          
    despesa_para_efetivar.save()

    messages.success(request, f'Despesa Efetivada com sucesso.')
    return redirect('lista-despesas-efetivadas')
  
#ok  
def despesas_estornar(request, despesa_id):
    # Obtém a instância da Despesa a ser editada
    despesa_para_estornar = get_object_or_404(Despesa, id=despesa_id)

    # Verifica se o usuário logado é o proprietário da Despesa
    if despesa_para_estornar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-despesas')
    
    # Verifica se o status da Despesa é "Registrado"
    if despesa_para_estornar.despesa_status == 'Registrado':
        messages.error(request, 'Não é possível estornar uma Despesa registrada.')
        return redirect('lista-despesas')
    
    despesa_para_estornar.debito_ja_realizado = 'Não'
    despesa_para_estornar.despesa_status = 'Registrado'

    conta_para_atualizar = Conta.objects.get(id=despesa_para_estornar.conta_debito_id)
    conta_para_atualizar.saldo += despesa_para_estornar.valor # Estorna o valor na conta escolhida
    
    conta_para_atualizar.save()          
    despesa_para_estornar.save()

    messages.success(request, f'Despesa Estornada com sucesso. Status: "Registrado".')
    return redirect('lista-despesas-registradas')
 
#ok   
def editar_despesa(request, despesa_id): # Premissa: despesa não efetivada, ou seja, despesa registrada!

    # Obtém a instância da Despesa a ser editada
    despesa_para_editar = get_object_or_404(Despesa, id=despesa_id)
    print("Entrou em editar_despesa.")
    # Verifica se o usuário logado é o proprietário da Despesa
    if despesa_para_editar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-despesas')
    print("A despesa é do Usuário que está logado.")
    # Verifica se o status da Despesa é "Efetivado"
    if despesa_para_editar.despesa_status == 'Efetivado':
        messages.error(request, 'Não é possível editar uma Despesa efetivada.')
        return redirect('lista-despesas')
    print("A despesa está Registrada.")
    form = DespesaForms(request.user, instance=despesa_para_editar)
    
    if request.method == 'POST':
        form = DespesaForms(request.user, request.POST, instance=despesa_para_editar)
        if form.is_valid():
            form.save()                   
            messages.success(request, 'Despesa editada com sucesso.')
            return redirect('lista-despesas')
    return render(request, 'operacoes/despesa-editar.html', {'form_editar_despesa': form, 'despesa_id': despesa_id})

#ok
def deletar_despesa(request, despesa_id): #falta criar uma logica para confirmar se realmente quer deletar a despesa
    # Obtém a instância da Despesa a ser deletada
    despesa_para_deletar = get_object_or_404(Despesa, id=despesa_id)

    # Verifica se o usuário logado é o proprietário da Despesa
    if despesa_para_deletar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-despesas')

    if despesa_para_deletar.debito_ja_realizado == 'Sim':
        conta_para_atualizar = Conta.objects.get(id=despesa_para_deletar.conta_debito_id)
        conta_para_atualizar.saldo += despesa_para_deletar.valor #estorna o valor debitado
        conta_para_atualizar.save()
        messages.success(request, f'Despesa deletada com sucesso e o saldo da conta "{conta_para_atualizar.descricao}" foi atualizado.')

    else:
        # Se não houver atualização de saldo, exibe apenas a mensagem de deleção
        messages.success(request, 'Despesa deletada com sucesso.')
    
    despesa_para_deletar.delete()
    return redirect('lista-despesas')

def despesa_detalhada(request, despesa_id):

    # Obtém a instância da Despesa a ser editada
    despesa_para_detalhar = get_object_or_404(Despesa, id=despesa_id)
    
    # Verifica se o usuário logado é o proprietário da Despesa
    if despesa_para_detalhar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-despesas')
   
    #form = DespesaForms(request.user, instance=despesa_para_detalhar)
    
    hoje = datetime.now().replace(hour=0, minute=0, second=1, microsecond=999999).date()
    data_da_despesa = despesa_para_detalhar.data.replace(hour=23, minute=59, second=59, microsecond=999999).date()
    

    # print(">>>>>>>>>>>>>>>>>>>>>>>>", hoje)
    # print("------------------------", data_da_despesa)

    # Cores
    verde = '#AFF6A6'
    vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    if despesa_para_detalhar.despesa_status == 'Registrado': 
        #if (despesa_para_detalhar.data.replace(tzinfo=None) < hoje):
        if (data_da_despesa < hoje):
            condicao = 'Atrasada'
            cor = vermelho
        elif (data_da_despesa == hoje):
            condicao = 'Vence Hoje'
            cor = amarelo
        else:
            condicao = 'No Prazo'
            cor = azul
    else:
        condicao = 'Paga'
        cor = verde
    
    print("------------------------", condicao)

    return render(request, 'operacoes/despesa-detalhada.html', {'despesa': despesa_para_detalhar, 'condicao': condicao, 'cor': cor})  