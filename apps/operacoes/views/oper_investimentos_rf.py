from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import timedelta, datetime, timezone
from apps.configuracoes.models import Conta, CorretoraInvestimento
from apps.operacoes.models import InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada
from apps.operacoes.forms import InvestimentoRendaFixaForms, ResgateRendaFixaForms
from django.db.models import Case, Value, When, CharField

# ----------------------------- Investimentos ------------------------------------

#ok
def investimentos_todos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").all()
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("proprietario").all()
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("proprietario").all()
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        renda_variavel_cadastradas = InvestimentoRendaVariavel.objects.order_by("-data_investimento").filter(proprietario_id=request.user)
        previdencia_privada_cadastradas = InvestimentoPrevidenciaPrivada.objects.order_by("-data_investimento").filter(proprietario_id=request.user)  
        
    return render(
        request,
        'operacoes/index-investimentos.html',
        {
            "lista_renda_fixa": renda_fixa_cadastradas,
            "lista_renda_variavel": renda_variavel_cadastradas,
            "lista_previdencia_privada": previdencia_privada_cadastradas,
        }
    )


# ----------------------- Investimentos Renda Fixa --------------------------------

#ok
def investimentos_rf_todos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").all()
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user)

    # Define a data de hoje
    hoje = datetime.now().date()

    # Cores
    verde = '#AFF6A6'
    #vermelho = '#F49185'
    amarelo = '#F6f66f' 
    azul = '#9EDEF0'

    # Atribui cores às despesas com base na data usando annotate
    renda_fixa_cadastradas = renda_fixa_cadastradas.annotate(
        cor=Case(
            When(investimento_status='Registrado', then=Value(amarelo)),
            When(investimento_status='Ativo', then=Value(verde)),
            default=Value(azul),
            output_field=CharField(), 
        )
    )

    return render(
        request,
        'operacoes/index-investimentos_rf.html',
        {
            "lista_renda_fixa": renda_fixa_cadastradas,

        }
    )

#ok
def investimentos_rf_registrados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").filter(investimento_status='Registrado')
        
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Registrado')
    
    if len(renda_fixa_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Fixa com status: Registrado!")
        return redirect('lista-investimento-rf')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_fixa_cadastradas = renda_fixa_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )
        # return render(request, 'operacoes/invest-rf-registrados.html', {"lista_renda_fixa": renda_fixa_cadastradas,})
        return render(request, 'operacoes/index-investimentos_rf.html', {"lista_renda_fixa": renda_fixa_cadastradas,})

#ok
def investimentos_rf_ativos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").filter(investimento_status='Ativo')
        
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Ativo')
    
    if len(renda_fixa_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Fixa com status: Ativo!")
        return redirect('lista-investimento-rf')
    else:
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_fixa_cadastradas = renda_fixa_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )
        return render(request, 'operacoes/index-investimentos_rf.html', {"lista_renda_fixa": renda_fixa_cadastradas,})
        # return render(request, 'operacoes/invest-rf-ativos.html', {"lista_renda_fixa": renda_fixa_cadastradas,})

#ok
def investimentos_rf_liquidados(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("proprietario").filter(investimento_status='Liquidado')
        
    else:
        renda_fixa_cadastradas = InvestimentoRendaFixa.objects.order_by("-data_investimento").filter(proprietario_id=request.user, investimento_status='Liquidado')
    
    if len(renda_fixa_cadastradas) == 0:
        messages.error(request, "Não há Investimento em Renda Fixa com status: Liquidado!")
        return redirect('lista-investimento-rf')
    else:
        # return render(request, 'operacoes/invest-rf-ativos.html', {"lista_renda_fixa": renda_fixa_cadastradas,})
        # Cores
        verde = '#AFF6A6'
        #vermelho = '#F49185'
        amarelo = '#F6f66f' 
        azul = '#9EDEF0'

        # Atribui cores às despesas com base na data usando annotate
        renda_fixa_cadastradas = renda_fixa_cadastradas.annotate(
            cor=Case(
                When(investimento_status='Registrado', then=Value(amarelo)),
                When(investimento_status='Ativo', then=Value(verde)),
                default=Value(azul),
                output_field=CharField(), 
            )
        )
        return render(request, 'operacoes/index-investimentos_rf.html', {"lista_renda_fixa": renda_fixa_cadastradas,})

#ok
def novo_investimento_rf(request):
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
        form = InvestimentoRendaFixaForms(request.user, request.POST)
        if form.is_valid():
            novo_investimento = form.save(commit=False)
            novo_investimento.proprietario = request.user
            novo_investimento.data_registro -= timedelta(hours=4)
            

            if ((novo_investimento.investimento_debitado_em_conta == 'Sim') and (novo_investimento.data_investimento <= novo_investimento.data_registro)):
                novo_investimento.investimento_status = 'Ativo'
                valor = novo_investimento.valor_investido
                corretagem_aplicacao = novo_investimento.taxas_corretagem_aplicacao
                irpf_aplicacao = novo_investimento.irpf_aplicacao
                corretora_para_atualizar = CorretoraInvestimento.objects.get(id=novo_investimento.corretora_id)
                conta_para_atualizar = Conta.objects.get(id=novo_investimento.conta_debito_id)
                
                conta_para_atualizar.saldo -= (valor + corretagem_aplicacao + irpf_aplicacao) #debita da conta fonte do recurso
                corretora_para_atualizar.saldo += valor #credita na corretora que foi realizado o investimento
                
                conta_para_atualizar.save()
                corretora_para_atualizar.save()

                mensagem = 'Novo Investimento em Renda Fixa cadastrado com sucesso. Status do Investimento: "Ativo".'
            else:
                novo_investimento.investimento_debitado_em_conta = 'Não'
                novo_investimento.investimento_status = 'Registrado'
                novo_investimento.data_resgate = '9999-12-31 00:00:00.000000'
                mensagem = 'Novo Investimento em Renda Fixa cadastrado com sucesso. Status do Investimento: "Registrado". Efetive o investimento para atualizar os saldos da conta e da corretora de investimento.'

            novo_investimento.save()

            messages.success(request, mensagem)
            return redirect('lista-investimento-rf')
        else:
            print(form.errors)
    else:
        form =InvestimentoRendaFixaForms(request.user)

    return render(request, 'operacoes/invest-rf-novo.html', {'form_novo_investimento': form})

#ok
def efetivar_investimento_rf(request, investimento_rf_id):
    # Obtém a instância do Investimento a ser editado
    investimento_para_efetivar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_efetivar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-investimento-rf')
    
    # Verifica se o status do Investimento é diferente de "Registrado". Podendo ser 'Ativo' ou 'Liquidado'.
    if investimento_para_efetivar.investimento_status != 'Registrado':
        messages.error(request, 'Não é possível efetivar um Investimento já efetivado.')
        return redirect('lista-investimento-rf')
    
    # Verifica se a data do Investimento é uma Data Futura.
    if datetime.now(timezone.utc) < investimento_para_efetivar.data_investimento:
        messages.error(request, 'Não é possível Efetivar um Investimento com data futura. Seu Investimento continua com o status de "Registrado".')       
        return redirect('lista-investimento-rf')
   
    investimento_para_efetivar.investimento_debitado_em_conta = 'Sim'
    investimento_para_efetivar.investimento_status = 'Ativo'

    valor = investimento_para_efetivar.valor_investido
    taxas = investimento_para_efetivar.taxas_corretagem_aplicacao
    irpf = investimento_para_efetivar.irpf_aplicacao

    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_efetivar.corretora_id)
    conta_para_atualizar = Conta.objects.get(id=investimento_para_efetivar.conta_debito_id)
    
    conta_para_atualizar.saldo -= (valor + taxas + irpf) #debita da conta fonte do recurso
    corretora_para_atualizar.saldo += valor #credita na corretora que foi realizado o investimento
    
    conta_para_atualizar.save()
    corretora_para_atualizar.save()           
    investimento_para_efetivar.save()

    messages.success(request, f'Investimento em Renda Fixa Efetivado com sucesso. Status do Investimento: Investimento Ativo. Valor debitado da Conta "{conta_para_atualizar.descricao}" e creditado na Corretora "{corretora_para_atualizar.descricao}"')
    return redirect('lista-investimento-rf')

#ok
def resgatar_renda_fixa(request, investimento_rf_id): 
    # Obtém a instância do Investimento a ser editado
    investimento_para_resgatar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_resgatar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-investimento-rf')
    
    # Verifica se o status do Investimento é diferente de "Ativo". Podendo ser 'Ativo' ou 'Liquidado'.
    if investimento_para_resgatar.investimento_status != 'Ativo':
        messages.error(request, 'Só é permitido resgatar um Investimento Ativo.')
        return redirect('lista-investimento-rf')
    
    form = ResgateRendaFixaForms(request.user, instance=investimento_para_resgatar)

    if request.method == 'POST':
        form = ResgateRendaFixaForms(request.user, request.POST, instance=investimento_para_resgatar)
        if form.is_valid():
            investimento_resgatado = form.save(commit=False)

            dt_investimento = investimento_resgatado.data_investimento
            dt_vencimento = investimento_resgatado.data_vencimento
            dt_resgate = investimento_resgatado.data_resgate
            dt_hoje = datetime.now(timezone.utc)

            # Verifica se a data do Resgate do Investimento é antes da data de Investimento, Após a data de Vencimento ou Maior que a data de hoje.
            
            if (dt_resgate > dt_hoje) and (dt_resgate <= dt_vencimento):
                messages.error(request, 'Não é permitido o resgate de Investimento com Data Futura. Seu Investimento continua com o status de "Ativo".')       
                return redirect('lista-investimento-rf')
            
            elif dt_resgate < dt_investimento:
                messages.error(request, 'Não é permitido o resgate de Investimento com Data inferior à Data do Investimento. Seu Investimento continua com o status de "Ativo".')       
                return redirect('lista-investimento-rf')
            
            elif dt_resgate > dt_vencimento:
                messages.error(request, 'Não é permitido o resgate de Investimento com Data superior à Data de Vencimento. Seu Investimento continua com o status de "Ativo".')       
                return redirect('lista-investimento-rf')
            
            else:
                corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_resgatado.corretora_id)               
                lucro_bruto = investimento_resgatado.valor_resgate_liquido - investimento_resgatado.valor_investido
                corretora_para_atualizar.saldo += lucro_bruto        
                corretora_para_atualizar.save()
                investimento_resgatado.investimento_status = 'Liquidado'
                investimento_resgatado.save()                      
                messages.success(request, 'Resgate realizado com sucesso. Status: Liquidado.')    
            
            return redirect('lista-investimento-rf')
     
    return render(request, 'operacoes/renda-fixa-resgatar.html', {'form_resgatar_rf': form, 'investimento_rf_id': investimento_rf_id})

#ok
def editar_investimento_rf(request, investimento_rf_id):

    # Obtém a instância do Investimento a ser editado
    investimento_para_editar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_editar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rf')
    
    # Verifica se o status do Investimento é diferente de "Liquidado". Para editar um investimento Liquidado primeiro é necessário Reativar o investimento, cancelando o Resgate do Investimento, o que o faz retornar ao status de ativo.
    if investimento_para_editar.investimento_status == 'Liquidado':
        messages.error(request, 'Não é possível editar um Investimento Liquidado. Reative o Investimento e faça as alterações desejadas.')
        return redirect('lista-investimento-rf')

    valor_investido_original = investimento_para_editar.valor_investido
    conta_debito_original = investimento_para_editar.conta_debito_id
    corretora_credito_original = investimento_para_editar.corretora_id
    taxas_original = investimento_para_editar.taxas_corretagem_aplicacao
    irpf_original = investimento_para_editar.irpf_aplicacao

    form = InvestimentoRendaFixaForms(request.user, instance=investimento_para_editar)
    
    if request.method == 'POST':
       
        form = InvestimentoRendaFixaForms(request.user, request.POST, instance=investimento_para_editar)
        
        if form.is_valid():
            investimento_editado = form.save(commit=False)
            investimento_editado.data_registro -= timedelta(hours=4)

            if investimento_editado.investimento_debitado_em_conta == 'Sim': # O valor já havia sido creditado na conta.

                # Verifica se houve mudança de um dos seguintes atributos: valor, Conta, Corretora, Taxas ou IRPF.
                if ((investimento_editado.valor_investido != valor_investido_original) or 
                    (investimento_editado.conta_debito_id != conta_debito_original) or 
                    (investimento_editado.corretora_id != corretora_credito_original) or
                    (investimento_editado.taxas_corretagem_aplicacao != taxas_original) or
                    (investimento_editado.irpf_aplicacao != irpf_original)
                    ): 
                    
                    # Estorna os valores originais que foram debitados da Conta.
                    conta_para_atualizar_original = Conta.objects.get(id=conta_debito_original)
                    conta_para_atualizar_original.saldo += (valor_investido_original + taxas_original + irpf_original) 
                    conta_para_atualizar_original.save()
                    
                    # Debita da Conta as informações do investimento_editado: Valor, Taxas e IRPF.
                    conta_para_atualizar_nova = Conta.objects.get(id=investimento_editado.conta_debito_id)
                    conta_para_atualizar_nova.saldo -= (investimento_editado.valor_investido + investimento_editado.taxas_corretagem_aplicacao + investimento_editado.irpf_aplicacao)
                    conta_para_atualizar_nova.save()

                    # Estorna o valor original que havia sido creditado na Corretora.
                    corretora_para_atualizar_original = CorretoraInvestimento.objects.get(id=corretora_credito_original)
                    corretora_para_atualizar_original.saldo -= valor_investido_original 
                    corretora_para_atualizar_original.save()

                    # Credita o valor do investimento existente no forms editado pelo user na Corretora
                    corretora_para_atualizar_nova = CorretoraInvestimento.objects.get(id=investimento_editado.corretora_id)
                    corretora_para_atualizar_nova.saldo += investimento_editado.valor_investido
                    corretora_para_atualizar_nova.save()
            
            # else: não precisa desse else pois se o valor ainda não havia sido debitado em conta não importam os valores / conta/ corretora que o usuário digitar, bastando salvar tudo com as novas informações lançadas.
        
            investimento_editado.save()                  
                
            messages.success(request, 'Investimento editado com sucesso.')
            return redirect('lista-investimento-rf') 
        
    return render(request, 'operacoes/invest-rf-editar.html', {'form_editar_investimento': form, 'investimento_rf_id': investimento_rf_id})

#ok
def reativar_investimento_rf(request, investimento_rf_id):
    # Obtém a instância do Investimento a ser editado
    investimento_para_reativar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_reativar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Despesas de outros usuários.')
        return redirect('lista-investimento-rf')
    
    # Verifica se o status do Investimento é diferente de "Liquidado"
    if investimento_para_reativar.investimento_status != 'Liquidado':
        messages.error(request, 'Só é permitido reativar um Investimento Liquidado.')
        return redirect('lista-investimento-rf')

    valor_investimento_original = investimento_para_reativar.valor_investido
    print("Investimento Original: ", valor_investimento_original)
    valor_resgatado_original = investimento_para_reativar.valor_resgate_liquido
    print("Resgate Original: ", valor_resgatado_original)
    lucro_teorico = valor_resgatado_original - valor_investimento_original
    print("Lucro Teórico: ", lucro_teorico)
    
    investimento_para_reativar.investimento_status = 'Ativo'
    investimento_para_reativar.irpf_resgate = 0
    investimento_para_reativar.taxas_corretagem_resgate = 0
    investimento_para_reativar.data_resgate = '9999-12-31 00:00:00.000000'
    investimento_para_reativar.valor_resgate_liquido = 0

       
    # Debita na Corretora o lucro que havia sido creditado no resgate original do investimento
    corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_reativar.corretora_id)
    print("Saldo Inicial da Corretora: ", corretora_para_atualizar.saldo)
    corretora_para_atualizar.saldo -= lucro_teorico 
    print("Saldo Atualizado da Corretora: ", corretora_para_atualizar.saldo)
    corretora_para_atualizar.save()

    investimento_para_reativar.save()

    messages.success(request, f'Investimento em Renda Fixa Reativado com sucesso. Status do Investimento: Investimento Ativo.')
    return redirect('lista-investimento-rf')

#ok
def deletar_investimento_rf(request, investimento_rf_id):
     # Obtém a instância do Investimento a ser deletado
    investimento_para_deletar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)

    # Verifica se o usuário logado é o proprietário do Investimento
    if investimento_para_deletar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rf')
    
    if investimento_para_deletar.investimento_status == 'Ativo':
        
        corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_deletar.corretora_id)
        conta_para_atualizar = Conta.objects.get(id=investimento_para_deletar.conta_debito_id)
        valor_investimento_inicial = investimento_para_deletar.valor_investido
        taxas = investimento_para_deletar.taxas_corretagem_aplicacao
        irpf = investimento_para_deletar.irpf_aplicacao
        
        # Estorna valores na conta fonte do recurso
        conta_para_atualizar.saldo += (valor_investimento_inicial + taxas + irpf)

        # Debita valor na corretora que foi realizado o investimento
        corretora_para_atualizar.saldo -= valor_investimento_inicial 
        
        conta_para_atualizar.save()
        corretora_para_atualizar.save()

    elif investimento_para_deletar.investimento_status == 'Liquidado':
        
        corretora_para_atualizar = CorretoraInvestimento.objects.get(id=investimento_para_deletar.corretora_id)
        conta_para_atualizar = Conta.objects.get(id=investimento_para_deletar.conta_debito_id)
        valor_investimento_inicial = investimento_para_deletar.valor_investido
        valor_investimento_resgate = investimento_para_deletar.valor_resgate_liquido
        lucro_teorico = valor_investimento_resgate - valor_investimento_inicial
        taxas = investimento_para_deletar.taxas_corretagem_aplicacao
        irpf = investimento_para_deletar.irpf_aplicacao
        
        # Estorna valores na conta fonte do recurso
        conta_para_atualizar.saldo += (valor_investimento_inicial + taxas + irpf)

        # Debita valor na corretora que foi realizado o investimento
        corretora_para_atualizar.saldo -= (valor_investimento_inicial + lucro_teorico)
        
        conta_para_atualizar.save()
        corretora_para_atualizar.save()

    else:
        # Se não houver atualização de saldo em Conta nem na Corretora, exibe apenas a mensagem de deleção
        pass
        
    investimento_para_deletar.delete()
    messages.success(request, 'Investimento em Renda Fixa deletado com sucesso.')

    return redirect('lista-investimento-rf')

def retornar_para_registro_rf(request, investimento_rf_id):
    pass

def investimento_rf_detalhado(request, investimento_rf_id):

    # Obtém a instância da Despesa a ser editada
    investimento_para_detalhar = get_object_or_404(InvestimentoRendaFixa, id=investimento_rf_id)
    
    # Verifica se o usuário logado é o proprietário da Despesa
    if investimento_para_detalhar.proprietario != request.user:
        messages.error(request, 'Não é possível acessar Investimentos de outros usuários.')
        return redirect('lista-investimento-rf')
   
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

    return render(request, 'operacoes/invest-rf-detalhado.html', {'investimento': investimento_para_detalhar, 'cor': cor})  