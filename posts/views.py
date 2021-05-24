import django
from django.db import connection
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
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

class PostDetalhes(View):
    template_name = 'posts/post_detalhes.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, publicado_post=True)
        # Criando um dicionário com os objetos utilizados no template para não precisar alterar o template
        self.contexto = {
            'post': post,
            'comentarios': Comentario.objects.filter(post_comentario=post, publicado_comentario=True),
            'form': FormComentario(request.POST or None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        form = self.contexto['form']

        if not form.is_valid():
            return render(request, self.template_name, self.contexto)
        
        # Validado o formulário, mas ainda não salvando na base de dados
        comentario = form.save(commit=False)

        if request.user.is_authenticated:
            comentario.usuario_comentario = request.user
        
        comentario.post_comentario = self.contexto['post']
        comentario.save()
        messages.success(request, 'Comentário enviado')
        return redirect('post_detalhes', pk=self.kwargs.get('pk'))