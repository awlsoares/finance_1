from django.shortcuts import redirect
from django.urls import reverse

class NoLoginMiddleware:
    print("Entrou em NoLogin")
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Se o usuário estiver logado, redirecione para a página de logout
            return redirect(reverse('logout'))  # Certifique-se de ter uma URL chamada 'logout'

        response = self.get_response(request)
        print("Response:", response)
        return response
