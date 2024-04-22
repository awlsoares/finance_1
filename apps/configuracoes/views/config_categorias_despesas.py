from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.configuracoes.models import CategoriaDespesa
from apps.configuracoes.forms import CategoriaDespesaForms
from apps.operacoes.models import Despesa
 
def categorias_despesas(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!") 
                return redirect('login')

        if request.user.is_superuser:
                categorias_cadastradas = CategoriaDespesa.objects.all().order_by("proprietario", "descricao")
        else:
                categorias_cadastradas = CategoriaDespesa.objects.filter(proprietario_id=request.user.id).order_by("descricao")
        
        return render(request, 'configuracoes/index-categorias-despesas.html', {"lista_categorias": categorias_cadastradas})

def nova_categoria_despesa(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
        
        if request.method == 'POST':
                formulario_nova_categoria = CategoriaDespesaForms(request.user, request.POST) 
                if formulario_nova_categoria.is_valid():
                        nova_categoria = formulario_nova_categoria.save(commit=False)
                        nova_categoria.proprietario = request.user
                        nova_categoria.descricao = nova_categoria.descricao.upper()
                        if CategoriaDespesa.objects.filter(descricao=nova_categoria.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Esta categoria já existe para o usuário.')
                                return render(request, 'configuracoes/nova-categoria-desp.html', {'form_nova_categoria': formulario_nova_categoria})
                        nova_categoria.save()
                        messages.success(request, 'Nova categoria de despesa cadastrada com sucesso.')
                        return redirect('lista-categorias-despesas')
        else:
                formulario_nova_categoria = CategoriaDespesaForms(request.user)

        return render(request, 'configuracoes/nova-categoria-desp.html', {'form_nova_categoria': formulario_nova_categoria})

def editar_categoria_despesa(request, categoria_id):
        categoria_para_editar = get_object_or_404(CategoriaDespesa, id=categoria_id)
        
        print("ID da Função: ", categoria_id," Editar: ", categoria_para_editar, " ID da Cat Despesa: ", categoria_para_editar.id)
        
        form = CategoriaDespesaForms(request.user, instance=categoria_para_editar) # colocar antes do return

        if request.method == 'POST':
                form = CategoriaDespesaForms(request.user, request.POST, instance=categoria_para_editar)
                if form.is_valid():
                        nova_categoria = form.save(commit=False)
                        nova_categoria.descricao = nova_categoria.descricao.upper() 
                        if CategoriaDespesa.objects.filter(descricao=nova_categoria.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Esta categoria já existe para o usuário.')
                                return render(request, 'configuracoes/editar-categoria-despesa.html', {'form_editar_categoria': form, 'categoria_id': categoria_id})
                        
                        nova_categoria.save() #salva no banco de dados
                        messages.success(request, 'Categoria editada com sucesso.')

                        return redirect('lista-categorias-despesas')
        
        return render(request, 'configuracoes/editar-categoria-despesa.html', {'form_editar_categoria': form, 'categoria_id': categoria_id})

def deletar_categoria_despesa(request, categoria_id):
        categoria_para_deletar = get_object_or_404(CategoriaDespesa, id=categoria_id)
        
        print("ID da Função: ", categoria_id," Deletar: ", categoria_para_deletar, " ID da Cat Despesa: ", categoria_para_deletar.id)


        qtd_despesas = len(Despesa.objects.filter(proprietario_id=request.user, categoria_id=categoria_para_deletar.id))

        if qtd_despesas == 0:
                categoria_para_deletar.delete()
                messages.success(request, f'Categoria "{categoria_para_deletar.descricao}" deletada com sucesso.')
        else:
                mensagem = f'Há {qtd_despesas} despesa(s) criada(s) na categoria "{categoria_para_deletar.descricao}" e por isso não é possível efetivar a exclusão da mesma.'
                messages.error(request, mensagem)
                print(mensagem)
        return redirect('lista-categorias-despesas')