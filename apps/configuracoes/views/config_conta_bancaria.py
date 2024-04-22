from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.configuracoes.models import Conta
from apps.operacoes.models import Receita, Despesa, InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada
from apps.configuracoes.forms import ContaForms
from datetime import timedelta

def index(request):
        if not request.user.is_authenticated:
                #messages.error(request, "Usuário não logado!")
                
                mensagem_tipo = "erro"
                mensagem_conteudo = "Usuário não logado!"
                return redirect('login')
                #return render(request, 'usuarios/login.html', {"mensagem_tipo": mensagem_tipo, "mensagem_conteudo": mensagem_conteudo})
        
        return render(request, 'base/index_base.html')
             
def contas(request):
        
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
               
        if request.user.is_superuser:
                contas_cadastradas = Conta.objects.all().order_by("proprietario", "descricao")
        else:
                contas_cadastradas = Conta.objects.filter(proprietario_id=request.user.id).order_by("descricao")
        
        return render(request, 'configuracoes/index-contas.html', {"lista_contas": contas_cadastradas})

def nova_conta(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
        
        if request.method == 'POST':
                formulario_nova_conta = ContaForms(request.user, request.POST) 
                if formulario_nova_conta.is_valid():
                        nova_conta = formulario_nova_conta.save(commit=False)
                        nova_conta.proprietario = request.user
                        nova_conta.data_registro_conta -= timedelta(hours=4)
                        nova_conta.descricao = nova_conta.descricao.upper()
                        if Conta.objects.filter(descricao=nova_conta.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Uma Conta com a mesma Descrição já existe para o usuário. Altere o a Descrição da Conta.')
                                print('Uma Conta com a mesma Descrição já existe para o usuário. Altere o a Descrição da Conta.')
                                return redirect('cadastrar-conta')
                                # return render(request, 'configuracoes/editar-conta.html', {'form3_editar_conta': form, 'conta_id': conta_id})
                        nova_conta.save()
                        messages.success(request, 'Nova conta cadastrada com sucesso.')
                        return redirect('lista-contas')
        else:
                formulario_nova_conta = ContaForms(request.user) 

        return render(request, 'configuracoes/nova-conta.html', {'form2_nova_conta': formulario_nova_conta})

def editar_conta(request, conta_id):
        conta_para_editar = get_object_or_404(Conta, id=conta_id)

        form = ContaForms(request.user, instance=conta_para_editar)

        if request.method == 'POST':
                form = ContaForms(request.user, request.POST, instance=conta_para_editar)
                if form.is_valid():
                        conta_editada = form.save(commit=False)
                        conta_editada.descricao = conta_editada.descricao.upper()    
                        conta_editada.save() #salva no banco de dados
                        messages.success(request, 'Conta editada com sucesso.')
                        
                        return redirect('lista-contas')
                
        return render(request, 'configuracoes/editar-conta.html', {'form3_editar_conta': form, 'conta_id': conta_id})

def deletar_conta(request, conta_id):
        conta_para_deletar = get_object_or_404(Conta, id=conta_id)
        
        qtd_receitas_nesta_conta = len(Receita.objects.filter(proprietario_id=request.user, conta_credito_id=conta_para_deletar.id))
        qtd_despesas_nesta_conta = len(Despesa.objects.filter(proprietario_id=request.user, conta_debito_id=conta_para_deletar.id))
        qtd_invest_rf_nesta_conta = len(InvestimentoRendaFixa.objects.filter(proprietario_id=request.user, conta_debito_id=conta_para_deletar.id))
        qtd_invest_rv_nesta_conta = len(InvestimentoRendaVariavel.objects.filter(proprietario_id=request.user, conta_debito_id=conta_para_deletar.id))
        qtd_invest_prev_nesta_conta = len(InvestimentoPrevidenciaPrivada.objects.filter(proprietario_id=request.user, conta_debito_id=conta_para_deletar.id))

        qtd_total = qtd_receitas_nesta_conta + qtd_despesas_nesta_conta + qtd_invest_rf_nesta_conta + qtd_invest_rv_nesta_conta + qtd_invest_prev_nesta_conta
       
        if qtd_total == 0:
                conta_para_deletar.delete()
                messages.success(request, f'Conta "{conta_para_deletar.descricao}" deletada com sucesso.')

        else:
                mensagem = f'Há {qtd_total} operação(ões) criada(s) na Conta "{conta_para_deletar.descricao}" e por isso não é possível efetivar a exclusão da mesma.'
                messages.error(request, mensagem)
                print(mensagem)
                
        return redirect('lista-contas')

def arquivar_conta(request, conta_id):
      
      # Nessa operação de arquivamento prever a existência de receitas ou despesas ainda Em Aberto (Registrado).
      # Opção 1, como Regra de Negócio, só arquivar com as receitas / despesas Efetivadas!
      
      pass