from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.configuracoes.models import CategoriaReceita
from apps.configuracoes.forms import CategoriaReceitaForms
from apps.operacoes.models import Receita

def categorias_receitas(request):

        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!") 
                return redirect('login')
                       
        if request.user.is_superuser:
                categorias_cadastradas = CategoriaReceita.objects.all().order_by("proprietario", "descricao")
        else:
                categorias_cadastradas = CategoriaReceita.objects.filter(proprietario_id=request.user.id).order_by("descricao")
        
        return render(request, 'configuracoes/index-categorias-receitas.html', {"lista_categorias": categorias_cadastradas})

def nova_categoria_receita(request):
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login')
        
        if request.method == 'POST':
                formulario_nova_categoria = CategoriaReceitaForms(request.user, request.POST) 
                if formulario_nova_categoria.is_valid():
                        nova_categoria = formulario_nova_categoria.save(commit=False)
                        nova_categoria.proprietario = request.user
                        nova_categoria.descricao = nova_categoria.descricao.upper()
                        if CategoriaReceita.objects.filter(descricao=nova_categoria.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Esta categoria já existe para o usuário.')
                                return render(request, 'configuracoes/nova-categoria-rec.html', {'form_nova_categoria': formulario_nova_categoria})
                        nova_categoria.save()
                        messages.success(request, 'Nova categoria de receita cadastrada com sucesso.')
                        return redirect('lista-categorias-receitas')
        else:
                formulario_nova_categoria = CategoriaReceitaForms(request.user)

        return render(request, 'configuracoes/nova-categoria-rec.html', {'form_nova_categoria': formulario_nova_categoria})

def editar_categoria_receita(request, categoria_id):
        categoria_para_editar = get_object_or_404(CategoriaReceita, id=categoria_id)
        
        print("ID da Função: ", categoria_id," Editar: ", categoria_para_editar, " ID da Cat Receita: ", categoria_para_editar.id)
        
        form = CategoriaReceitaForms(request.user, instance=categoria_para_editar) # colocar antes do return

        if request.method == 'POST':
                form = CategoriaReceitaForms(request.user, request.POST, instance=categoria_para_editar)
                if form.is_valid():
                        nova_categoria = form.save(commit=False)
                        print(nova_categoria)
                        nova_categoria.descricao = nova_categoria.descricao.upper() 
                        if CategoriaReceita.objects.filter(descricao=nova_categoria.descricao, proprietario=request.user).exists():
                                messages.error(request, 'Esta categoria já existe para o usuário.')
                                return render(request, 'configuracoes/editar-categoria-receita.html', {'form_editar_categoria': form, 'categoria_id': categoria_id})
                        
                        nova_categoria.save() #salva no banco de dados
                        messages.success(request, 'Categoria editada com sucesso.')

                        return redirect('lista-categorias-receitas')
        
        return render(request, 'configuracoes/editar-categoria-receita.html', {'form_editar_categoria': form, 'categoria_id': categoria_id})
        
def deletar_categoria_receita(request, categoria_id):
        categoria_para_deletar = get_object_or_404(CategoriaReceita, id=categoria_id)
        
        print("ID da Função: ", categoria_id," Deletar: ", categoria_para_deletar, " ID da Cat Receita: ", categoria_para_deletar.id)

        #categoria_para_deletar = CategoriaDespesa.objects.get(id=categoria_id)

        qtd_receitas = len(Receita.objects.filter(proprietario_id=request.user, categoria_id=categoria_para_deletar.id))

        if qtd_receitas == 0:
                categoria_para_deletar.delete()
                messages.success(request, f'Categoria "{categoria_para_deletar.descricao}" deletada com sucesso.')
        else:
                mensagem = f'Há {qtd_receitas} receita(s) criada(s) na categoria "{categoria_para_deletar.descricao}" e por isso não é possível efetivar a exclusão da mesma.'
                messages.error(request, mensagem)
                print(mensagem)

        return redirect('lista-categorias-receitas')