from .oper_receitas import *
from .oper_depesas import *
from .oper_depesas_cartao import *
from .oper_investimentos_rf import *
from .oper_investimentos_rv import *
from .oper_investimentos_prev import *
from .oper_transacoes import *

# Criar método para verificar na data de hoje se tem alguma fatura aberta que deveria estar fechada.
# Caso positivo providenciar o fechamento da fatura.
# Verificar se te alguma fatura que deveria estar aberta na data de hoje.
# Caso negativo providenciar a abertura de nova fatura.
# Essa lógica deverá iterar sob todos os cartões de crédito que estiverem cadastrados e ativos no sistema.