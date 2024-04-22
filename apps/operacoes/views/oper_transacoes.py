from django.shortcuts import render, redirect, get_object_or_404
from apps.configuracoes.models import Conta, CorretoraInvestimento, ContaPrevidenciaPrivada, CategoriaReceita, CategoriaDespesa
from apps.operacoes.models import Receita, InvestimentoRendaFixa, InvestimentoRendaVariavel, InvestimentoPrevidenciaPrivada, Despesa
from apps.operacoes.forms import ReceitaForms, InvestimentoRendaFixaForms, InvestimentoRendaVariavelForms, InvestimentoPrevidenciaPrivadaForms, ResgateRendaFixaForms, ResgateRendaVariavelForms, DespesaForms
from django.contrib import messages
from datetime import timedelta, date, datetime, timezone
from dateutil.relativedelta import relativedelta

# ----------------------- Operações entre as Contas / Corretoras --------------------------------

# transferência entre contas
# conta -> conta
# conta -> corretora
# corretora -> conta
# corretora -> corretora