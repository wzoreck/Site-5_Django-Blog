from django.db.models.query_utils import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q, Count, Case, When # por conta do qs.annotate
from .models import Post

# Create your views here.
class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6 # Número de objetos que irão aparecer por página
    context_object_name = 'posts' # Nomeando o nome da 'lista' que vai ser passada para o template, no for apresentamos cada post

    def get_queryset(self):
        qs = super().get_queryset()
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

class PostDetalhes(UpdateView):
    pass