from django.contrib import admin
from apps.configuracoes.models import Conta
from apps.operacoes.models import Receita
from apps.usuarios.models import Usuario

class ExibirContas(admin.ModelAdmin):
    list_display = ("id", "tipo", "proprietario_id", "descricao", "saldo", 
        "incluir_saldo_no_dashboard", "data_registro_conta")
    list_display_links = ("id","descricao")
    search_fields = ("tipo", "descricao")
    list_filter = ("tipo",)
    list_editable = ("incluir_saldo_no_dashboard",)
    list_per_page = 10

class ExibirUsuarios(admin.ModelAdmin):
    list_display = ("id", "nome", "data_nascimento", "email", "foto", "proprietario_id")
    list_display_links = ("id","nome")
    search_fields = ("nome",)
    list_filter = ("nome",)
    list_per_page = 10

# class ExibirReceitas(admin.ModelAdmin):
#     list_display = ("id", "proprietario_id", "categoria_id", "data", "valor",
#         "descricao", "conta_credito_id", "credito_ja_realizado", "data_registro")
#     list_display_links = ("id","descricao")
#     search_fields = ("descricao",)
#     list_filter = ("proprietario_id",)
#     list_editable = ("credito_ja_realizado",)
#     list_per_page = 10

admin.site.register(Conta, ExibirContas)
# admin.site.register(Receita, ExibirReceitas)
admin.site.register(Usuario, ExibirUsuarios)


