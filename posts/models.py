from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    titulo_post = models.CharField(max_length=150, verbose_name='Título') # verbose_name é para setar qual o nome aparecerá na tabela admin
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data Publicação')
    conteudo_post = models.TextField(verbose_name='Conteúdo Post')
    excerto_post = models.TextField(verbose_name='Excerto')
    categoria_post = models.ForeignKey(Categoria, models.DO_NOTHING, blank=True, null=True, verbose_name='Categoria') # Desta forma podemos criar um post sem categoria
    image_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    publicado_post = models.BooleanField(default=False, verbose_name='Público')

    def __str__(self):
        return self.titulo_post