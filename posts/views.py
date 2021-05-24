import django
from django.db import connection
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q, Count, Case, When # por conta do qs.annotate
from .models import Post
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages

# Create your views here.
class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6 # Número de objetos que irão aparecer por página
    context_object_name = 'posts' # Nomeando o nome da 'lista' que vai ser passada para o template, no for apresentamos cada post

    def get_queryset(self):
        qs = super().get_queryset()
        # Para otimizar as consultas sql, estavam sendo feitas muitas por conta do campo categoria_post
        qs = qs.select_related('categoria_post') 
        qs = qs.order_by('-id').filter(publicado_post=True) # Ordenando de forma decrescente pelo id
        # .filter(publicado_post=True) para exibir apenas os Posts marcados como publicados

        # Funciona como um IF, para contar apenas os comentarios publicado_comentario=True 
        qs  = qs.annotate(
            num_comentario=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1) # then=1 conta 1
                )
            ) 
        )
        return qs
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['connection'] = connection

        return contexto


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs

class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs

class PostDetalhes(UpdateView): # UpdateView espera um formulário, não esta sendo feito isso agr, mas é o correto
    template_name = 'posts/post_detalhes.html'
    model = Post
    # Estamos pegando/aproveitando o formulário lá do app comentarios
    form_class = FormComentario
    # Nome para acessarmos o post no template
    context_object_name = 'post'

    # Validação do formulário de cometário post, aqui que vamos criar o objeto comentário!!!
    def form_valid(self, form):
        post = self.get_object()
        # Enquanto não criar o comentário e mandar salvar não vai salvar
        comentario = Comentario(**form.cleaned_data)
        # Terminar de atribuir dados ao objeto comentario (Campos que faltaram)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user
        
        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso')
        
        return redirect('post_detalhes', pk=post.id) # pk é como foi definido na url

    # Para aparecer apenas os comentários publicados
    def get_context_data(self, **kwargs):
        # O contexto é o Post que injetado no template
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        # Comentarios vindos da base de dados, a serem exibidos no template
        comentarios = Comentario.objects.filter(publicado_comentario=True, post_comentario=post.id)

        contexto['comentarios'] = comentarios
        
        return contexto