from django.urls import path

from .views import *

# from apps.operacoes.views import (
#     receitas_todas, despesas_todas, investimentos_todos, investimentos_rf_todos, investimentos_rv_todos, investimentos_prev_todos,
    
#     nova_receita, nova_receita_recorrente, efetivar_receita, devolver_receita, editar_receita, deletar_receita, receitas_registradas, receitas_efetivadas, receitas_atrasadas, receitas_futuras, 
    
#     despesa_nova, nova_despesa_recorrente, despesas_efetivar, despesas_estornar, editar_despesa, deletar_despesa, despesas_registradas, despesas_efetivadas, despesas_atrasadas, despesas_futuras,

#     novo_investimento_rf, efetivar_investimento_rf, resgatar_renda_fixa, editar_investimento_rf, reativar_investimento_rf,   investimentos_rf_registrados, investimentos_rf_ativos, investimentos_rf_liquidados, deletar_investimento_rf,

#     novo_investimento_rv, efetivar_investimento_rv, resgatar_renda_variavel, editar_investimento_rv, reativar_investimento_rv, investimentos_rv_registrados, investimentos_rv_ativos, investimentos_rv_liquidados,  
    
#     novo_investimento_previdencia, efetivar_investimento_prev, editar_investimento_prev, investimentos_prev_registrados, investimentos_prev_ativos
# )

urlpatterns = [
        path('receitas/index', receitas_todas, name='lista-receitas'),
        path('receitas/registradas/', receitas_registradas, name='lista-receitas-registradas'),
        path('receitas/efetivadas/', receitas_efetivadas, name='lista-receitas-efetivadas'),
        path('receitas/atrasadas/', receitas_atrasadas, name='lista-receitas-atrasadas'),
        path('receitas/futuras', receitas_futuras, name='lista-receitas-futuras'),
        path('receitas/mes-atual/', receitas_do_mes_atual, name='lista-receitas-do-mes-atual'),
        path('receitas/mes-anterior/', receitas_do_mes_anterior, name='lista-receitas-do-mes-anterior'),
        path('receitas/mes-proximo/', receitas_do_mes_proximo, name='lista-receitas-do-mes-proximo'),
        path('receitas/cadastrar/unica', nova_receita, name='receita-cadastrar'),
        path('receitas/cadastrar/recorrente', nova_receita_recorrente, name='receita-cadastrar-recorrente'),
        path('receitas/efetivar/<int:receita_id>', efetivar_receita, name='receita-efetivar'),
        path('receitas/devolver/<int:receita_id>', devolver_receita, name='receita-devolver'),
        path('receitas/editar/<int:receita_id>', editar_receita, name='receita-editar'),
        path('receitas/deletar/<int:receita_id>', deletar_receita, name='receita-deletar'),  
        path('receitas/index/detalhes/<int:receita_id>', receita_detalhada, name='receita-detalhada'),    
        
        path('despesas/index/', despesas_todas, name='lista-despesas'),
        path('despesas/cadastrar', despesa_nova, name='despesa-cadastrar'),
        path('despesas/cadastrar/recorrente', nova_despesa_recorrente, name='despesa-cadastrar-recorrente'),
        path('despesas/registradas/', despesas_registradas, name='lista-despesas-registradas'),
        path('despesas/efetivadas/', despesas_efetivadas, name='lista-despesas-efetivadas'),
        path('despesas/atrasadas/', despesas_atrasadas, name='lista-despesas-atrasadas'),
        path('despesas/futuras/', despesas_futuras, name='lista-despesas-futuras'),
        path('despesas/mes-atual/', despesas_do_mes_atual, name='lista-despesas-do-mes-atual'),
        path('despesas/mes-anterior/', despesas_do_mes_anterior, name='lista-despesas-do-mes-anterior'),
        path('despesas/mes-proximo/', despesas_do_mes_proximo, name='lista-despesas-do-mes-proximo'),
        path('despesas/efetivar/<int:despesa_id>', despesas_efetivar, name='despesa-efetivar'),
        path('despesas/estornar/<int:despesa_id>', despesas_estornar, name='despesa-estornar'),
        path('despesas/editar/<int:despesa_id>', editar_despesa, name='despesa-editar'),
        path('despesas/deletar/<int:despesa_id>', deletar_despesa, name='despesa-deletar'),
        path('despesas/index/detalhes/<int:despesa_id>', despesa_detalhada, name='despesa-detalhada'), 

        
        path('investimentos/index', investimentos_todos, name='lista-investimentos'),

        path('investimentos/rf/index/', investimentos_rf_todos, name='lista-investimento-rf'),
        path('investimentos/rf/novo/', novo_investimento_rf, name='cadastrar-investimento-rf'),
        path('investimentos/rf/registrados/', investimentos_rf_registrados, name='rf-registrados'),
        path('investimentos/rf/ativos/', investimentos_rf_ativos, name='rf-ativos'),
        path('investimentos/rf/liquidados/', investimentos_rf_liquidados, name='rf-liquidados'),
        path('investimentos/rf/efetivar/<int:investimento_rf_id>', efetivar_investimento_rf, name='rf-efetivar'),
        path('investimentos/rf/resgatar/<int:investimento_rf_id>', resgatar_renda_fixa, name='rf-resgatar'),
        path('investimentos/rf/reativar/<int:investimento_rf_id>', reativar_investimento_rf, name='rf-reativar'),
        path('investimentos/rf/editar/<int:investimento_rf_id>', editar_investimento_rf, name='rf-editar'),
        path('investimentos/rf/deletar/<int:investimento_rf_id>', deletar_investimento_rf, name='rf-deletar'),
        path('investimentos/rf/detalhes/<int:investimento_rf_id>', investimento_rf_detalhado, name='rf-detalhado'),
        
        
        path('investimentos/rv/index/', investimentos_rv_todos, name='lista-investimento-rv'),
        path('investimentos/rv/novo/', novo_investimento_rv, name='cadastrar-investimento-rv'),
        path('investimentos/rv/registrados/', investimentos_rv_registrados, name='rv-registrados'),
        path('investimentos/rv/ativos/', investimentos_rv_ativos, name='rv-ativos'),
        path('investimentos/rv/liquidados/', investimentos_rv_liquidados, name='rv-liquidados'),
        path('investimentos/rv/efetivar/<int:investimento_rv_id>', efetivar_investimento_rv, name='rv-efetivar'),
        path('investimentos/rv/resgatar/<int:investimento_rv_id>', resgatar_renda_variavel, name='rv-resgatar'),
        path('investimentos/rv/reativar/<int:investimento_rv_id>', reativar_investimento_rv, name='rv-reativar'),
        path('investimentos/rv/editar/<int:investimento_rv_id>', editar_investimento_rv, name='rv-editar'),
        path('investimentos/rv/detalhes/<int:investimento_rv_id>', investimento_rv_detalhado, name='rv-detalhado'),

        path('investimentos/prev/index/', investimentos_prev_todos, name='lista-investimento-prev'), 
        path('investimentos/prev/novo/', novo_investimento_previdencia, name='cadastrar-investimento-prev'), 
        path('investimentos/prev/registrados/', investimentos_prev_registrados, name='prev-registrados'),
        path('investimentos/prev/ativos/', investimentos_prev_ativos, name='prev-ativos'),
        path('investimentos/prev/efetivar/<int:investimento_prev_id>', efetivar_investimento_prev, name='prev-efetivar'),
        path('investimentos/prev/editar/<int:investimento_prev_id>', editar_investimento_prev, name='prev-editar'),
        path('investimentos/prev/detalhes/<int:investimento_prev_id>', investimento_prev_detalhado, name='prev-detalhado'),

        path('cartao/despesas/nova', nova_despesa_cartao, name='cartao-nova-despesa'),
        path('cartao/fatura/parcial', gerar_fatura_parcial, name='cartao-fatura-parcial'),
        #path('cartao/fatura/parcial-cartao', fatura_parcial_cartao, name='cartao-fatura-parcial_2'),
]