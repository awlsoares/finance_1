from django.shortcuts import render, redirect, get_object_or_404
from apps.configuracoes.models import ContaPrevidenciaPrivada
from apps.operacoes.models import InvestimentoPrevidenciaPrivada
from apps.configuracoes.forms import ContaPrevidenciaPrivadaForms
from django.contrib import messages
from datetime import timedelta

def contas_previdencia_privada(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
               
        if request.user.is_superuser:
                contas_previdencia_cadastradas = ContaPrevidenciaPrivada.objects.all().order_by("proprietario", "descricao")
        else:
                contas_previdencia_cadastradas = ContaPrevidenciaPrivada.objects.filter(proprietario_id=request.user.id).order_by("descricao")
        
        return render(request, 'configuracoes/index-contas-previdencia-privada.html', {"lista_contas_previdencia_privada": contas_previdencia_cadastradas})

def nova_conta_previdencia_privada(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
        
        if request.method == 'POST':
                formulario_nova_conta_previdencia = ContaPrevidenciaPrivadaForms(request.user, request.POST) 
                if formulario_nova_conta_previdencia.is_valid():
                        nova_conta_previdencia = formulario_nova_conta_previdencia.save(commit=False)
                        nova_conta_previdencia.proprietario = request.user
                        nova_conta_previdencia.data_registro_previdencia -= timedelta(hours=4)
                        nova_conta_previdencia.descricao = nova_conta_previdencia.descricao.upper()
                        if ContaPrevidenciaPrivada.objects.filter(descricao=nova_conta_previdencia.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Esta Conta de Previdência já existe para o usuário.')
                                return redirect('cadastrar-conta-previdencia-privada')
                        nova_conta_previdencia.save()
                        messages.success(request, 'Nova Conta de Previdência Privada cadastrada com sucesso.')
                        return redirect('lista-contas-previdencia-privada')
        else:
                formulario_nova_conta_previdencia = ContaPrevidenciaPrivadaForms(request.user)

        return render(request, 'configuracoes/nova-conta-previdencia-privada.html', {'form_nova_conta_previdencia_privada': formulario_nova_conta_previdencia})

def editar_conta_previdencia_privada(request, previdencia_id):
        conta_prev_para_editar = get_object_or_404(ContaPrevidenciaPrivada, id=previdencia_id) 

        form = ContaPrevidenciaPrivadaForms(request.user, instance=conta_prev_para_editar)

        if request.method == 'POST':
                form = ContaPrevidenciaPrivadaForms(request.user, request.POST, instance=conta_prev_para_editar)
                if form.is_valid():
                        previdencia_editada = form.save(commit=False)
                        previdencia_editada.descricao = previdencia_editada.descricao.upper()    
                        previdencia_editada.save() #salva no banco de dados
                        messages.success(request, 'Conta de Previdência Privada editada com sucesso.')
                        
                        return redirect('lista-contas-previdencia-privada')
                
        return render(request, 'configuracoes/editar-conta-previdencia.html', {'form3_editar_conta_previdencia': form, 'previdencia_id': previdencia_id})

def deletar_conta_previdencia_privada(request, previdencia_id):
        previdencia_para_deletar = get_object_or_404(ContaPrevidenciaPrivada, id=previdencia_id)
        
        qtd_invest_prev_nesta_conta = len(InvestimentoPrevidenciaPrivada.objects.filter(proprietario_id=request.user, conta_previdencia_id=previdencia_para_deletar.id))
       
        if qtd_invest_prev_nesta_conta == 0:
                previdencia_para_deletar.delete()
                messages.success(request, f'Corretora "{previdencia_para_deletar.descricao}" deletada com sucesso.')

        else:
                mensagem = f'Há {qtd_invest_prev_nesta_conta} Investimento(s) criad(s) na Conta de Previdëncia "{previdencia_para_deletar.descricao}" e por isso não é possível efetivar a exclusão da mesma.'
                messages.error(request, mensagem)
                print(mensagem)
                
        return redirect('lista-contas-previdencia-privada')

def arquivar_conta_previdencia(request, previdencia_id):
      
      # Nessa operação de arquivamento prever a existência de Investimentos em Previdênciao em Aberto.
      # Opção 1, como Regra de Negócio, só arquivar com os Investimentos Efetivados.
      
      pass