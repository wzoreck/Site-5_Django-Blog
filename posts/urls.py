from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'), # views.PostIndex.as_view() para chamar a classe em views.py como uma view
    path('categoria/<str:categoria>', views.PostCategoria.as_view(), name='post_categoria'), # Vai receber uma string na url
    path('busca/', views.PostBusca.as_view(), name='post_busca'),
    path('post/<int:pk>', views.PostDetalhes.as_view(), name='post_detalhes'), # Vai receber o id do post (ao inves de pk poderia ser id)
]
