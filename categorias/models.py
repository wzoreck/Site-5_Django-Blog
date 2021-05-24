from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Categoria(models.Model):
    nome_cat = models.CharField(max_length=50)

    # Com esse metodo quando formos exibir uma categoria no template seja exibido o nome caso ela esteja como chave estrangeira em outra classe, ex: {{ post.categoria_post }} categoria_post é ForeignKey
    def __str__(self):
        return self.nome_cat