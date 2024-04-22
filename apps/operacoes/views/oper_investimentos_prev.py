from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, datetime, timezone
from apps.configuracoes.models import Conta, ContaPrevidenciaPrivada
from apps.operacoes.models import InvestimentoPrevidenciaPrivada
from apps.operacoes.forms import InvestimentoPrevidenciaPrivadaForms
from django.db.models import Case, Value, When, CharField


# ----------------------- Investimentos Previdência Privada --------------------------------

#ok
def investimentos_prev_todos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").all()
    else:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user)  
    
    # Cores
    verde = '#AFF6A6'
    #vermelho = '#F49185'
    amarelo = '#F6f66f' 
    #azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    previdencia_privada_cadastradas = previdencia_privada_cadastradas.annotate(
        cor=Case(
            When(investimento_status='Registrado', then=Value(amarelo)),
            default=Value(verde),
            output_field=CharField(), 
        )
    )

    return render(
        request,
        'operacoes/index-investimentos_prev.html',
        {
            "lista_previdencia_privada": previdencia_privada_cadastradas,
        }
    )

#ok
def investimentos_prev_registrados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").filter(investimento_status='Registrado')
        
    else:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Registrado')
    
    if len(previdencia_privada_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Previdência Privada com status: Registrado!")
        return redirect('lista-investimento-prev')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        #azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        previdencia_privada_cadastradas = previdencia_privada_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                default=Value(verde),
                output_field=CharField(), 
            )
        )

        return render(request, 'operacoes/index-investimentos_prev.html', {"lista_previdencia_privada": previdencia_privada_cadastradas,})

#ok
def investimentos_prev_ativos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").filter(investimento_status='Efetivado')
        
    else:
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Efetivado')
    
    if len(previdencia_privada_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Previdência Privada com status: Ativo!")
        return redirect('lista-investimento-prev')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        #azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        previdencia_privada_cadastradas = previdencia_privada_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                default=Value(verde),
                output_field=CharField(), 
            )
        )

        return render(request, 'operacoes/index-investimentos_prev.html', {"lista_previdencia_privada": previdencia_privada_cadastradas,})
 
def novo_investimento_previdencia(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    quantidade_contas_previdencia = len(ContaPrevidenciaPrivada.objects.filter(proprietario=request.user))
    if quantidade_contas_previdencia == 0:
        messages.error(request, "Para registrar um investimento em Previdência você precisa de uma Conta de Previdência!")
        return redirect('cadastrar-conta-previdencia-privada')
    
    quantidade__contas = len(Conta.objects.filter(proprietario=request.user))
    if quantidade__contas == 0:
        messages.error(request, "Para registrar um investimento em Previdência você precisa de uma Conta para débito do Investimento!")
        return redirect('cadastrar-conta')

    if request.method == 'POST':
        form = InvestimentoPrevidenciaPrivadaForms(request.user, request.POST)
        if form.is_valid():
            novo_investimento = form.save(commit=False)
            novo_investimento.proprietario = request.user
            novo_investimento.data_registro -= timedelta(hours=4)

            if ((novo_investimento.investimento_debitado_em_conta == 'Sim') and (novo_investimento.data_investimento <= novo_investimento.data_registro)):
                novo_investimento.investimento_status = 'Ativo'
                valor = novo_investimento.valor_investido
                conta_previdencia_para_atualizar = ContaPrevidenciaPrivada.objects.get(id=novo_investimento.conta_previdencia_id)
                conta_para_atualizar = Conta.objects.get(id=novo_investimento.conta_debito_id)
                
                conta_para_atualizar.saldo -= valor #debita da conta fonte do recurso
                conta_previdencia_para_atualizar.saldo += valor #credita na conta de previdencia que foi realizado o investimento
                
                conta_para_atualizar.save()
                conta_previdencia_para_atualizar.save()
               
                mensagem = 'Novo Investimento em Renda Variável cadastrado com sucesso. Status do Investimento: Investimento Ativo.'
            else:
                novo_investimento.investimento_debitado_em_conta = 'Não'
                novo_investimento.investimento_status = 'Registrado'
                
                mensagem = 'Novo Investimento em Previdência Privada cadastrado com sucesso. Status do Investimento: Registrado. Efetive o investimento para atualizar os saldos das Contas.'

            novo_investimento.save()

            messages.success(request, mensagem)
            return redirect('lista-investimento-prev')
        else:
            print(form.errors)
    else:
        form =InvestimentoPrevidenciaPrivadaForms(request.user)

    return render(request, 'operacoes/invest-prev-novo.html', {'form_novo_investimento': form})

#ok
def efetivar_investimento_prev(request, investimento_prev_id):
    # Obtém a instância do Investimento a ser editado
    investimento_para_efetivar = get_object_or_404(InvestimentoPrevidenciaPrivada, id=investimento_prev_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_efetivar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('index')
    
    # Verifica se o status do Investimento é diferente de "Registrado". Podendo ser 'Ativo' ou 'Liquidado'.
    if investimento_para_efetivar.investimento_status != 'Registrado':
        messages.error(request, 'Não é possível efetivar um Investimento já efetivado.')
        return redirect('lista-investimento-prev')
    
    # Verifica se a data do Investimento é uma Data Futura.
    if datetime.now(timezone.utc) < investimento_para_efetivar.data_investimento:
        messages.error(request, 'Não é possível Efetivar um Investimento com data futura. Seu Investimento continua com o status de "Registrado".')       
        return redirect('lista-investimento-prev')
    
    investimento_para_efetivar.investimento_debitado_em_conta = 'Sim'
    investimento_para_efetivar.investimento_status = 'Ativo'

    valor = investimento_para_efetivar.valor_investido

    conta_previdencia_para_atualizar = ContaPrevidenciaPrivada.objects.get(id=investimento_para_efetivar.conta_previdencia_id)
    conta_para_atualizar = Conta.objects.get(id=investimento_para_efetivar.conta_debito_id)
    
    conta_para_atualizar.saldo -= valor #debita da conta fonte do recurso
    conta_previdencia_para_atualizar.saldo += valor #credita na conta de previdencia que foi realizado o investimento
    
    conta_para_atualizar.save()
    conta_previdencia_para_atualizar.save()
    
    conta_para_atualizar.save()
    conta_previdencia_para_atualizar.save()           
    investimento_para_efetivar.save()

    messages.success(request, f'Investimento em Previdência Privada Efetivado com sucesso. Status do Investimento: Investimento Ativo. Valor debitado da Conta "{conta_para_atualizar.descricao}" e creditado na Previdência "{conta_previdencia_para_atualizar.descricao}"')

    return redirect('lista-investimento-prev')

def editar_investimento_prev(request, investimento_prev_id): 
    # Obtém a instância do Investimento a ser editado
    investimento_para_editar = get_object_or_404(InvestimentoPrevidenciaPrivada, id=investimento_prev_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_editar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-prev')
    
    valor_investido_original = investimento_para_editar.valor_investido
    conta_debito_original = investimento_para_editar.conta_debito_id
    conta_prev_credito_original = investimento_para_editar.conta_previdencia_id
    investimento_debitado_em_conta_original = investimento_para_editar.investimento_debitado_em_conta

    form = InvestimentoPrevidenciaPrivadaForms(request.user, instance=investimento_para_editar)
    
    if request.method == 'POST':
        print('Entrou em if request Post')
        form = InvestimentoPrevidenciaPrivadaForms(request.user, request.POST, instance=investimento_para_editar)
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

                    conta_prev_para_atualizar = ContaPrevidenciaPrivada.objects.get(id=investimento_editado.conta_previdencia_id)
                    conta_prev_para_atualizar.saldo += valor_investido_editado
                    conta_prev_para_atualizar.save()

                else: # O status mudará para Registrado . Precisa estornar o valor que foi debitado originalmente da conta original (pois no novo forms o usuário pode ter selecionado um novo valor, uma nova conta para débito e/ou uma nova corretora para crédito), independentemente do valor e da conta da receita editada.

                    investimento_editado.investimento_status = 'Registrado'
                    conta_para_atualizar = Conta.objects.get(id=conta_debito_original)
                    conta_para_atualizar.saldo += valor_investido_original
                    conta_para_atualizar.save()

                    conta_prev_para_atualizar = ContaPrevidenciaPrivada.objects.get(id=conta_prev_credito_original)
                    conta_prev_para_atualizar.saldo -= valor_investido_original
                    conta_prev_para_atualizar.save()

            else: # Não houve mudança no status do investimento, continuando Ativo ou Registrado.

                if investimento_editado.investimento_debitado_em_conta == 'Sim': # O valor já havia sido creditado na conta.

                    if ((investimento_editado.valor_investido != valor_investido_original) or 
                        (investimento_editado.conta_debito_id != conta_debito_original) or 
                        (investimento_editado.conta_previdencia_id != conta_prev_credito_original)): 
                        # Houve mudança de Valor, mudança Conta ou mudança da Conta de Previdëncia Privada.

                        conta_para_atualizar = Conta.objects.get(id=conta_debito_original)
                        conta_para_atualizar.saldo += valor_investido_original # estorna o valor original que havia sido debitado em conta.
                        conta_para_atualizar.saldo -= investimento_editado.valor_investido # debita o valor existente no forms editado pelo user.
                        conta_para_atualizar.save()

                        conta_prev_para_atualizar = ContaPrevidenciaPrivada.objects.get(id=conta_prev_credito_original)
                        conta_prev_para_atualizar.saldo -= valor_investido_original # estorna o valor original que havia sido creditado na corretora.
                        conta_prev_para_atualizar.saldo += investimento_editado.valor_investido #credita o valor do investimento existente no forms editado pelo user
                        conta_prev_para_atualizar.save()
                
                # else: não precisa desse else pois se o valor ainda não havia sido debitado em conta, nem no forms original nem no forms editado, não importa os valores / conta/ corretora que o usuário digitar, bastando salvar tudo com as novas informações lançadas.
                        
            investimento_editado.save()                   
                
            messages.success(request, 'Investimento editado com sucesso.')
            return redirect('lista-investimento-prev')
    return render(request, 'operacoes/invest-prev-editar.html', {'form_editar_investimento': form, 'investimento_prev_id': investimento_prev_id})

def deletar_investimento_prev(request, investimento_prev_id):
    pass

def retornar_para_registro_investimento_prev(request, investimento_prev_id):
    pass

def investimento_prev_detalhado(request, investimento_prev_id):

    # Obtém a instância da Despesa a ser editada
    investimento_para_detalhar = get_object_or_404(InvestimentoPrevidenciaPrivada, id=investimento_prev_id)
    
    # Verifica se o usuário logado é o proprietário da Despesa
    if investimento_para_detalhar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-prev')
   
    # Cores
    verde = '#AFF6A6'
    #vermelho = '#F49185'
    amarelo = '#F6f66f' 
    #azul = '#9EDEF0'

    if investimento_para_detalhar.investimento_status == 'Registrado': 
        cor = amarelo
    else:
        cor = verde
    
    # print("------------------------", condicao)

    return render(request, 'operacoes/invest-prev-detalhado.html', {'investimento': investimento_para_detalhar, 'cor': cor})  