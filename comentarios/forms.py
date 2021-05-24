from django.db.models import fields
from django.forms import ModelForm
from .models import Comentario

class FormComentario(ModelForm):
    # Para fazermos a verificação dos dados e exibir avisos/erros
    def clean(self):
        # Pegar os dados do formulário
        data = self.cleaned_data
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')
        
        if len(nome) < 5:
            # Informa o campo e a mensagem que irá ser renderizada
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais que 5 caracteres!'
            )

    class Meta:
        # Campos presente em models->Comentario que irão aparecer no formulário
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')