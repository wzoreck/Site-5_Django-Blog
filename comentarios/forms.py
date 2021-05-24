from django.db.models import fields
from django.forms import ModelForm
from .models import Comentario

class FormComentario(ModelForm):
    class Meta:
        # Campos presente em models->Comentario que irão aparecer no formulário
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')