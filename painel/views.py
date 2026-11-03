import calendar
from datetime import datetime
from decimal import Decimal, InvalidOperation
from re import fullmatch

import requests
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics

from .models import RegistroCotacao
from .serializers import RegistroCotacaoSerializer


def _seis_meses_atras(data):
    mes = data.month - 6
    ano = data.year
    if mes <= 0:
        mes += 12
        ano -= 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return data.replace(year=ano, month=mes, day=dia)


def _data_personalizada(valor):
    if not valor or not fullmatch(r'\d{2}/\d{2}/\d{4}', valor):
        raise ValueError('Informe a data no formato DD/MM/AAAA.')
    try:
        data = datetime.strptime(valor, '%d/%m/%Y').date()
    except ValueError as exc:
        raise ValueError('Informe uma data válida.') from exc

    hoje = timezone.localdate()
    if not _seis_meses_atras(hoje) <= data <= hoje:
        raise ValueError(
            'A data deve estar entre hoje e os últimos 6 meses.'
        )
    return data


def _consultar_contexto(data_informada=None):
    contexto = {}
    data = None
    if data_informada:
        try:
            data = _data_personalizada(data_informada)
        except ValueError as exc:
            return {'erro': str(exc), 'data_consulta': data_informada}
    try:
        if data:
            resposta = requests.get(
                settings.COTACAO_HISTORICO_URL,
                params={
                    'start_date': data.strftime('%Y%m%d'),
                    'end_date': data.strftime('%Y%m%d'),
                },
                timeout=5,
            )
            registro_opcoes = {
                'consulta_personalizada': True,
                'data_consulta': data,
            }
        else:
            # timeout evita que a página fique esperando para sempre
            resposta = requests.get(settings.COTACAO_URL, timeout=5)
            registro_opcoes = {}
        resposta.raise_for_status()
        dados = resposta.json()
        if isinstance(dados, list):
            cotacao = dados[-1]
        else:
            cotacao = dados.get('USDBRL', dados)
        valor = Decimal(cotacao['bid'])
        registro = RegistroCotacao.objects.create(
            valor=valor,
            **registro_opcoes,
        )
        contexto = {
            'sucesso': True,
            'registro': registro,
            'data_consulta': data_informada or '',
        }
    except requests.exceptions.RequestException:
        contexto = {
            'erro': (
                'Não foi possível consultar a cotação agora. '
                'Tente novamente em instantes.'
            )
        }
    except (ValueError, KeyError, TypeError, InvalidOperation):
        # A API respondeu, mas em um formato inesperado.
        contexto = {
            'erro': 'A API externa respondeu em um formato inesperado.'
        }
    return contexto


def consultar_cotacao(request):
    return render(
        request,
        'painel/consultar.html',
        _consultar_contexto(request.GET.get('data_consulta')),
    )


def consultar_cotacao2(request):
    return render(
        request,
        'painel/consultar2.html',
        _consultar_contexto(request.GET.get('data_consulta')),
    )


class HistoricoCotacaoView(generics.ListAPIView):
    """Somente leitura: histórico do mais recente para o mais antigo."""
    serializer_class = RegistroCotacaoSerializer

    def get_queryset(self):

        return RegistroCotacao.objects.order_by('-data_hora_consulta', '-id')
# Create your views here.
