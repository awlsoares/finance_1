from django.urls import path

from .views import *

# from apps.configuracoes.views import index, nova_categoria_receita, nova_categoria_despesa, contas, nova_conta, editar_conta, deletar_conta, corretoras, nova_corretora, cartao, novo_cartao_credito, editar_cartao, deletar_cartao, categorias_receitas, editar_categoria_receita, deletar_categoria_receita, categorias_despesas, editar_categoria_despesa, deletar_categoria_despesa, contas_previdencia_privada, nova_conta_previdencia_privada

urlpatterns = [
        path('', index, name='index'),
        
        path('receitas/categoria/index/', categorias_receitas, name='lista-categorias-receitas'),
        path('receitas/categoria/cadastrar/', nova_categoria_receita, name='cadastrar-categoria-rec'),
        path('receitas/categoria/editar/<int:categoria_id>', editar_categoria_receita, name='editar-categoria-receita'),
        path('receitas/categoria/deletar/<int:categoria_id>', deletar_categoria_receita, name='deletar-categoria-receita'),

        path('despesas/categoria/index/', categorias_despesas, name='lista-categorias-despesas'),
        path('despesas/categoria/cadastrar/', nova_categoria_despesa, name='cadastrar-categoria-desp'),
        path('despesas/categoria/editar/<int:categoria_id>', editar_categoria_despesa, name='editar-categoria-despesa'),
        path('despesas/categoria/deletar/<int:categoria_id>', deletar_categoria_despesa, name='deletar-categoria-despesa'),

        path('contas/index/', contas, name='lista-contas'),
        path('contas/cadastrar/', nova_conta, name='cadastrar-conta'),
        path('contas/editar/<int:conta_id>', editar_conta, name='editar-conta'),        
        path('contas/deletar/<int:conta_id>', deletar_conta, name='deletar-conta'),
        
        path('cartao/index/', cartao, name='lista-cartoes'),
        path('cartao/cadastrar/', novo_cartao_credito, name='cadastrar-cartao'),
        path('cartao/editar/<int:cartao_id>', editar_cartao, name='editar-cartao'),
        path('cartao/deletar/<int:cartao_id>', deletar_cartao, name='deletar-cartao'),
        
        
        path('corretora/index/', corretoras, name='lista-corretoras'),
        path('corretora/nova', nova_corretora, name='cadastrar-corretora'),
        path('corretora/editar/<int:corretora_id>', editar_corretora, name='editar-corretora'),
        path('corretora/deletar/<int:corretora_id>', deletar_corretora, name='deletar-corretora'),
        
        path('conta-previdencia/index/', contas_previdencia_privada, name='lista-contas-previdencia-privada'),
        path('conta-previdencia/cadastrar', nova_conta_previdencia_privada, name='cadastrar-conta-previdencia-privada'),
        path('conta-previdencia/editar/<int:previdencia_id>', editar_conta_previdencia_privada, name='editar-conta-previdencia-privada'),
        path('conta-previdencia/deletar/<int:previdencia_id>', deletar_conta_previdencia_privada, name='deletar-conta-previdencia-privada'),
]