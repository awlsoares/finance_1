from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, datetime, timezone
from apps.configuracoes.models import Conta, CorretoraInvestimento
from apps.operacoes.models import InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada
from apps.operacoes.forms import InvestimentoRendaVariavelForms, ResgateRendaVariavelForms
from django.db.models import Case, Value, When, CharField

# ----------------------- Investimentos Renda Variável --------------------------------

#ok
def investimentos_rv_todos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").all()
    else:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user)

    # Cores
    verde = '#AFF6A6'
    #vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    renda_variavel_cadastradas = renda_variavel_cadastradas.annotate(
        cor=Case(
            When(investimento_status='Registrado', then=Value(amarelo)),
            When(investimento_status='Ativo', then=Value(verde)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    return render(
        request,
        'operacoes/index-investimentos_rv.html',
        {
            "lista_renda_variavel": renda_variavel_cadastradas,
        }
    )

#ok
def investimentos_rv_registrados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").filter(investimento_status='Registrado')
        
    else:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Registrado')
    
    if len(renda_variavel_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Variável com status: Registrado!")
        return redirect('lista-investimento-rv')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_variavel_cadastradas = renda_variavel_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )

        return render(request, 'operacoes/index-investimentos_rv.html', {"lista_renda_variavel": renda_variavel_cadastradas,})

#ok
def investimentos_rv_ativos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").filter(investimento_status='Ativo')
        
    else:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Ativo')

    if len(renda_variavel_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Variável com status: Ativo!")
        return redirect('lista-investimento-rv')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_variavel_cadastradas = renda_variavel_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )

        return render(request, 'operacoes/index-investimentos_rv.html', {"lista_renda_variavel": renda_variavel_cadastradas,})
 
#ok
def investimentos_rv_liquidados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").filter(investimento_status='Liquidado')
        
    else:
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Liquidado')

    if len(renda_variavel_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Variável com status: Liquidado!")
        return redirect('lista-investimento-rv')
    else:

        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_variavel_cadastradas = renda_variavel_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )
        
        return render(request, 'operacoes/index-investimentos_rv.html', {"lista_renda_variavel": renda_variavel_cadastradas,})

def novo_investimento_rv(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_coorretoras = len(CorretoraInvestimento.objects.filter(proprietario=request.user))
    if quantidade_coorretoras == 0:
        messages.error(request, "Para registrar um Investimento você precisa de uma Corretora de Investimento!")
        return redirect('cadastrar-corretora')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar um Investimento você precisa de uma Conta para débito do Investimento!")
        return redirect('cadastrar-conta')

    if request.method == 'POST':
        form = InvestimentoRendaVariavelForms(request.user, request.POST)
        if form.is_valid():
            novo_investimento = form.save(commit=False)
            novo_investimento.proprietario = request.user
            novo_investimento.data_registro -= timedelta(hours=4)         

            if ((novo_investimento.investimento_debitado_em_conta == 'Sim') and (novo_investimento.data_investimento <= novo_investimento.data_registro)):
                novo_investimento.investimento_status = 'Ativo'
                valor = novo_investimento.valor_investido
                corretora_para_atualizar = CorretoraInvestimento.objects.get(id=novo_investimento.corretora_id)
                conta_para_atualizar = Conta.objects.get(id=novo_investimento.conta_debito_id)
                
                conta_para_atualizar.saldo -= valor #debita da conta fonte do recurso
                corretora_para_atualizar.saldo += valor #credita na corretora que foi realizado o investimento
                
                conta_para_atualizar.save()
                corretora_para_atualizar.save()
               
                mensagem = 'Novo Investimento em Renda Variável cadastrado com sucesso. Status do Investimento: Investimento Ativo.'
            else:
                novo_investimento.investimento_debitado_em_conta = 'Não'
                novo_investimento.investimento_status = 'Registrado'
                
                mensagem = 'Novo Investimento em Renda Variável cadastrado com sucesso. Status do Investimento: Investimento Registrado. Efetive o investimento para atualizar os saldos da conta e da corretora de investimento.'

            novo_investimento.save()

            messages.success(request, mensagem)
            return redirect('lista-investimento-rv')
        else:
            print(form.errors)
    else:
        form =InvestimentoRendaVariavelForms(request.user)

    return render(request, 'operacoes/invest-rv-novo.html', {'form_novo_investimento': form}) 

#ok
def efetivar_investimento_rv(request, investimento_rv_id):
    # Obtém a instância do Investimento a ser editado
    investimento_para_efetivar = get_object_or_404(InvestimentoRendaVariavel, id=investimento_rv_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_efetivar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rv')
    
    # Verifica se o status do Investimento é diferente de "Registrado". Podendo ser 'Ativo' ou 'Liquidado'.
    if investimento_para_efetivar.investimento_status != 'Registrado':
        messages.error(request, 'Não é possível efetivar um Investimento já efetivado.')
        return redirect('lista-investimento-rv')
    
    # Verifica se a data do Investimento é uma Data Futura.
    if datetime.now(timezone.utc) < investimento_para_efetivar.data_investimento:
        messages.error(request, 'Não é possível Efetivar um Investimento com data futura. Seu Investimento continua com o status de "Registrado".')       
        return redirect('lista-investimento-rv')
    
    investimento_para_efetivar.investimento_debitado_em_conta = 'Sim'
    investimento_para_efetivar.investimento_status = 'Ativo'

    valor = investimento_para_efetivar.valor_investido

    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_efetivar.corretora_id)
    conta_para_atualizar = Conta.objects.get(id=investimento_para_efetivar.conta_debito_id)
    
    conta_para_atualizar.saldo -= valor #debita da conta fonte do recurso
    corretora_para_atualizar.saldo += valor #credita na corretora que foi realizado o investimento
    
    conta_para_atualizar.save()
    corretora_para_atualizar.save()           
    investimento_para_efetivar.save()

    messages.success(request, f'Investimento em Renda Variável Efetivado com sucesso. Status do Investimento: Investimento Ativo. Valor debitado da Conta "{conta_para_atualizar.descricao}" e creditado na Corretora "{corretora_para_atualizar.descricao}"')

    if request.user.is_authenticated and request.user.is_superuser:
        #renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").all()
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").all()
        #previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").all()
    else:
        #renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        #previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user)  
    return render(request, 'operacoes/index-investimentos_rv.html',
        {
            #"lista_renda_fixa": renda_fixa_cadastradas,
            "lista_renda_variavel": renda_variavel_cadastradas,
            #"lista_previdencia_privada": previdencia_privada_cadastradas,
        }
    )

def resgatar_renda_variavel(request, investimento_rv_id): 
    renda_variavel_para_resgatar = InvestimentoRendaVariavel.objects.get(id=investimento_rv_id)
    form = ResgateRendaVariavelForms(request.user, instance=renda_variavel_para_resgatar)

    if request.method == 'POST':
        form = ResgateRendaVariavelForms(request.user, request.POST, instance=renda_variavel_para_resgatar)
        if form.is_valid():
            investimento_resgatado = form.save(commit=False)
            corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_resgatado.corretora_id)
            resgate_liquido_menos_valor_investido = investimento_resgatado.valor_resgate_liquido - renda_variavel_para_resgatar.valor_investido
            corretora_para_atualizar.saldo += resgate_liquido_menos_valor_investido
            corretora_para_atualizar.save()
            renda_variavel_para_resgatar.investimento_status = 'Liquidado'
            investimento_resgatado.save()                      
            messages.success(request, 'Resgate realizado com sucesso.')
        return redirect('lista-investimento-rv')
    return render(request, 'operacoes/renda-variavel-resgatar.html', {'form_resgatar_rv': form, 'investimento_rv_id': investimento_rv_id})

def editar_investimento_rv(request, investimento_rv_id): 
    # Obtém a instância do Investimento a ser editado
    investimento_para_editar = get_object_or_404(InvestimentoRendaVariavel, id=investimento_rv_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_editar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rv')
    
    # Verifica se o status do Investimento é diferente de "Liquidado". Para editar um investimento Liquidado primeiro é necessário Reativar o investimento, cancelando o Resgate do Investimento, o que o faz retornar ao status de ativo.
    if investimento_para_editar.investimento_status == 'Liquidado':
        messages.error(request, 'Não é possível editar um Investimento Liquidado. Reative o Investimento e faça as alterações desejadas.')
        return redirect('lista-investimento-rv')
    
    valor_investido_original = investimento_para_editar.valor_investido
    conta_debito_original = investimento_para_editar.conta_debito_id
    corretora_credito_original = investimento_para_editar.corretora_id
    investimento_debitado_em_conta_original = investimento_para_editar.investimento_debitado_em_conta

    form = InvestimentoRendaVariavelForms(request.user, instance=investimento_para_editar)
    
    if request.method == 'POST':
        form = InvestimentoRendaVariavelForms(request.user, request.POST, instance=investimento_para_editar)
        if form.is_valid():
            investimento_editado = form.save(commit=False)
            investimento_editado.data_registro -= timedelta(hours=4)

            if (investimento_editado.investimento_debitado_em_conta != investimento_debitado_em_conta_original): #houve mudança de Não->Sim ou Sim->Não.
                
                if investimento_editado.investimento_debitado_em_conta == 'Sim':# O status mudará de Registrado para Ativo.
                    investimento_editado.investimento_status = 'Ativo'
                    valor_investido_editado = investimento_editado.valor_investido
                    conta_para_atualizar = Conta.objects.get(id=investimento_editado.conta_debito_id)
                    conta_para_atualizar.saldo -= valor_investido_editado
                    conta_para_atualizar.save()

                    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_editado.corretora_id)
                    corretora_para_atualizar.saldo += valor_investido_editado
                    corretora_para_atualizar.save()

                else: # O status mudará para Registrado . Precisa estornar o valor que foi debitado originalmente da conta original (pois no novo forms o usuário pode ter selecionado um novo valor, uma nova conta para débito e/ou uma nova corretora para crédito), independentemente do valor e da conta da receita editada.

                    investimento_editado.investimento_status = 'Registrado'
                    conta_para_atualizar = Conta.objects.get(id=conta_debito_original)
                    conta_para_atualizar.saldo += valor_investido_original
                    conta_para_atualizar.save()

                    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=corretora_credito_original)
                    corretora_para_atualizar.saldo -= valor_investido_original
                    corretora_para_atualizar.save()

            else: # Não houve mudança no status do investimento, continuando Ativo ou Registrado.

                if investimento_editado.investimento_debitado_em_conta == 'Sim': # O valor já havia sido creditado na conta.

                    if ((investimento_editado.valor_investido != valor_investido_original) or 
                        (investimento_editado.conta_debito_id != conta_debito_original) or 
                        (investimento_editado.corretora_id != corretora_credito_original)): 
                        # Houve mudança de Valor, mudança Conta ou mudança de Corretora.

                        conta_para_atualizar_original = Conta.objects.get(id=conta_debito_original)
                        conta_para_atualizar_original.saldo += valor_investido_original # estorna o valor original que havia sido debitado em conta.
                        conta_para_atualizar_original.save()
                        
                        conta_para_atualizar_nova = Conta.objects.get(id=investimento_editado.conta_debito_id)
                        conta_para_atualizar_nova.saldo -= investimento_editado.valor_investido # debita o valor existente no forms editado pelo user.
                        conta_para_atualizar_nova.save()

                        corretora_para_atualizar_original = CorretoraInvestimento.objects.get(id=corretora_credito_original)
                        corretora_para_atualizar_original.saldo -= valor_investido_original # devolve o valor original que havia sido creditado na corretora.
                        corretora_para_atualizar_original.save()

                        corretora_para_atualizar_nova = CorretoraInvestimento.objects.get(id=investimento_editado.corretora_id)
                        corretora_para_atualizar_nova.saldo += investimento_editado.valor_investido #credita o valor do investimento existente no forms editado pelo user
                        corretora_para_atualizar_nova.save()
                
                # else: não precisa desse else pois se o valor ainda não havia sido debitado em conta, nem no forms original nem no forms editado, não importa os valores / conta/ corretora que o usuário digitar, bastando salvar tudo com as novas informações lançadas.

            investimento_editado.save()                   
                
            messages.success(request, 'Investimento editado com sucesso.')
            return redirect('lista-investimento-rv') 
    return render(request, 'operacoes/invest-rv-editar.html', {'form_editar_investimento': form, 'investimento_rv_id': investimento_rv_id})

def reativar_investimento_rv(request, investimento_rv_id):
    investimento_para_reativar = InvestimentoRendaVariavel.objects.get(id=investimento_rv_id)
    investimento_para_reativar.investimento_debitado_em_conta = 'Sim'
    investimento_para_reativar.investimento_status = 'Ativo'
    investimento_para_reativar.irpf_resgate = 0
    investimento_para_reativar.taxas_corretagem_resgate = 0

    valor_investimento_original = investimento_para_reativar.valor_investido
    valor_resgatado_original = investimento_para_reativar.valor_resgate_liquido

    investimento_para_reativar.valor_resgate_liquido = 0
    
    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_reativar.corretora_id)
    corretora_para_atualizar.saldo -= valor_resgatado_original - valor_investimento_original #Debita na corretora o lucro que havia sido creditado no resgate do investimento
    corretora_para_atualizar.save()

    investimento_para_reativar.save()

    messages.success(request, f'Investimento em Renda Variável Reativado com sucesso. Status do Investimento: Investimento Ativo.')

    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").all()
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").all()
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").all()
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user)  
    return render(request, 'operacoes/index-investimentos.html',
        {
            "lista_renda_fixa": renda_fixa_cadastradas,
            "lista_renda_variavel": renda_variavel_cadastradas,
            "lista_previdencia_privada": previdencia_privada_cadastradas,
        }
    )

def deletar_investimento_rv(request, investimento_rv_id):
    pass

def retornar_para_registro_rv(request, investimento_rv_id):
    pass

def investimento_rv_detalhado(request, investimento_rv_id):

    # Obtém a instância da Despesa a ser editada
    investimento_para_detalhar = get_object_or_404(InvestimentoRendaVariavel, id=investimento_rv_id)
    
    # Verifica se o usuário logado é o proprietário da Despesa
    if investimento_para_detalhar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rv')
   
    # Cores
    verde = '#AFF6A6'
    #vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    if investimento_para_detalhar.investimento_status == 'Registrado': 
        cor = amarelo
    elif investimento_para_detalhar.investimento_status == 'Liquidado':
        cor = azul
    else:
        cor = verde
    
    # print("------------------------", condicao)

    return render(request, 'operacoes/invest-rv-detalhado.html', {'investimento': investimento_para_detalhar, 'cor': cor})