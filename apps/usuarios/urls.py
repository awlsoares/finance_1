from django.urls import path
from apps.usuarios.views import login, cadastro, logout

urlpatterns = [
    path('usuario/login', login, name='login'),
    path('usuario/cadastrar', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
]