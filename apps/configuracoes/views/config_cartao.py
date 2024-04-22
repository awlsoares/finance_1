from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.configuracoes.models import CartaoCredito
from apps.configuracoes.forms import CartaoCreditoForms
from datetime import timedelta

def cartao(request):
        
        if not request.user.is_authenticated:
                messages.error(request, "Usuário não logado!")
                return redirect('login') 
 
        if request.user.is_authenticated and request.user.is_superuser:
                cartoes_cadastrados = CartaoCredito.objects.order_by("proprietario").all()
        else:
                cartoes_cadastrados = CartaoCredito.objects.order_by("bandeira").filter(proprietario_id=request.user)
        
        return render(request, 'configuracoes/index-cartoes.html', {"lista_cartoes": cartoes_cadastrados})

def novo_cartao_credito(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado!")
        return redirect('login')

    if request.method == 'POST':
        formulario_novo_cartao = CartaoCreditoForms(request.user, request.POST)
        if formulario_novo_cartao.is_valid():
            novo_cartao = formulario_novo_cartao.save(commit=False)
            novo_cartao.proprietario = request.user
            novo_cartao.data_registro_cartao -= timedelta(hours=4)
            novo_cartao.limite_disponivel = novo_cartao.limite
            novo_cartao.descricao = novo_cartao.descricao.upper()
            if CartaoCredito.objects.filter(descricao=novo_cartao.descricao, proprietario=request.user).exists():
                messages.error(request, 'Um Cartão com a mesma Descrição já existe para o usuário. Altere o a Descrição do Cartão.')
                
                return redirect('lista-cartoes')
            novo_cartao.save()
            messages.success(request, 'Novo cartão de crédito cadastrado com sucesso.')
            return redirect('lista-cartoes')
        else:
            print(formulario_novo_cartao.errors)
    else:
        formulario_novo_cartao = CartaoCreditoForms(request.user)

    return render(request, 'configuracoes/novo-cartao-credito.html', {'form_novo_cartao': formulario_novo_cartao})

def editar_cartao(request, cartao_id):
        cartao_para_editar = get_object_or_404(CartaoCredito, id=cartao_id)
        
        form = CartaoCreditoForms(request.user, instance=cartao_para_editar)

        if request.method == 'POST':
                form = CartaoCreditoForms(request.user, request.POST, instance=cartao_para_editar)
                if form.is_valid():
                        cartao_editado = form.save(commit=False)
                        cartao_editado.descricao = cartao_editado.descricao.upper()    
                        form.save() #salva no banco de dados
                        messages.success(request, 'Cartão editado com sucesso.')
                        
                        return redirect('lista-cartoes')
                
        return render(request, 'configuracoes/editar-cartao.html', {'form_editar_cartao': form, 'cartao_id': cartao_id})

def deletar_cartao(request, cartao_id): #falta criar uma logica para confirmar se realmente quer deletar o cartao de credito
        cartao_para_deletar = get_object_or_404(CartaoCredito, id=cartao_id)
        cartao_para_deletar.delete()
        # Pendente construir a lógica para deletar o cartão
        # Dependerá da existência de despesas cadastradas no cartão.

        return redirect('lista-cartoes')

def arquivar_cartao(request, cartao_id):
      
      # Nessa operação de arquivamento prever a existência de despesas no cartão em aberto.
      # Opção 1, como Regra de Negócio, só arquivar com as despesas pagas.
      
      pass