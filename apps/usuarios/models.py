from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import os
from django.contrib.auth.models import User
from django.db import models

def caminho_foto(instance, filename):
    return os.path.join('fotos', str(instance.nome), filename)

class Usuario(models.Model):

    nome = models.CharField(max_length=200, null=False, blank=False)
    data_nascimento = models.DateField(default=timezone.now, blank=False)
    email = models.EmailField()
    foto = models.ImageField(upload_to=caminho_foto, blank=True)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=1)
  
    def __str__(self):
        return self.nome