from django.urls import path
from . import views

urlpatterns = [
    path('', views.consultar_cotacao, name='inicio'),
    path('consultar/', views.consultar_cotacao, name='consultar'),
    path('consultar2/', views.consultar_cotacao2, name='consultar2'),
    path(
        'api/historico/',
        views.HistoricoCotacaoView.as_view(),
        name='api-historico',
    ),
]
