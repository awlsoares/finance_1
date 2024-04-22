from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.configuracoes.models import CorretoraInvestimento
from apps.operacoes.models import InvestimentoRendaFixa, InvestimentoRendaVariavel
from apps.configuracoes.forms import CorretoraForms
from datetime import timedelta

def corretoras(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
               
        if request.user.is_superuser:
                corretoras_cadastradas = CorretoraInvestimento.objects.all().order_by("proprietario", "descricao")
        else:
                corretoras_cadastradas = CorretoraInvestimento.objects.filter(proprietario_id=request.user.id).order_by("descricao")
        
        return render(request, 'configuracoes/index-corretoras.html', {"lista_corretoras": corretoras_cadastradas})

def nova_corretora(request):
        print("Entrou em nova_corretora")
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
        
        if request.method == 'POST':  
                print("Entrou em POST")
                formulario_nova_corretora = CorretoraForms(request.user, request.POST)  
                if formulario_nova_corretora.is_valid():
                        print("Entrou em is_valid")
                        nova_corretora = formulario_nova_corretora.save(commit=False)
                        nova_corretora.proprietario = request.user
                        nova_corretora.data_registro_conta -= timedelta(hours=4)
                        nova_corretora.descricao = nova_corretora.descricao.upper()
                        if CorretoraInvestimento.objects.filter(descricao=nova_corretora.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Uma Corretora com a mesma Descrição já existe para o usuário. Altere o a Descrição da Corretora.')
                                return redirect('lista-corretoras')
                        nova_corretora.save()
                        messages.success(request, 'Nova Corretora de Investimentos cadastrada com sucesso.')
                        return redirect('lista-corretoras')
        else:
                print("Entrou no else")
                formulario_nova_corretora = CorretoraForms(request.user)

        return render(request, 'configuracoes/nova-corretora.html', {'form_nova_corretora': formulario_nova_corretora})

def editar_corretora(request, corretora_id):
        corretora_para_editar = get_object_or_404(CorretoraInvestimento, id=corretora_id)

        form = CorretoraForms(request.user, instance=corretora_para_editar)

        if request.method == 'POST':
                form = CorretoraForms(request.user, request.POST, instance=corretora_para_editar)
                if form.is_valid():
                        corretora_editada = form.save(commit=False)
                        corretora_editada.descricao = corretora_editada.descricao.upper()                        
                        corretora_editada.save() #salva no banco de dados
                        messages.success(request, 'Corretora editada com sucesso.')
                        
                        return redirect('lista-corretoras')
                
        return render(request, 'configuracoes/editar-corretora.html', {'form3_editar_corretora': form, 'corretora_id': corretora_id})

def deletar_corretora(request, corretora_id):
        corretora_para_deletar = get_object_or_404(CorretoraInvestimento, id=corretora_id)
        
        qtd_invest_rf_nesta_conta = len(InvestimentoRendaFixa.objects.filter(proprietario_id=request.user, corretora_id=corretora_para_deletar.id))
        qtd_invest_rv_nesta_conta = len(InvestimentoRendaVariavel.objects.filter(proprietario_id=request.user, corretora_id=corretora_para_deletar.id))

        qtd_total = qtd_invest_rf_nesta_conta + qtd_invest_rv_nesta_conta
       
        if qtd_total == 0:
                corretora_para_deletar.delete()
                messages.success(request, f'Corretora "{corretora_para_deletar.descricao}" deletada com sucesso.')

        else:
                mensagem = f'Há {qtd_total} Investimento(s) criad(s) na Corretora "{corretora_para_deletar.descricao}" e por isso não é possível efetivar a exclusão da mesma.'
                messages.error(request, mensagem)
                print(mensagem)
                
        return redirect('lista-corretoras')

def arquivar_corretora(request, corretora_id):
      
      # Nessa operação de arquivamento prever a existência de Investimentos Registrados, Ativos ou Liquidados
      # Opção 1, como Regra de Negócio, só arquivar com os Investimentos nas Corretoras com Status Liquidado.
      
      pass