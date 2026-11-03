# Pulse FX — Painel de Cotações

Aplicação Django que consulta a cotação USD/BRL na AwesomeAPI, salva as
consultas no banco e apresenta o histórico em uma interface original e em uma
interface visual alternativa com gráfico.

## Funcionalidades

- Consulta normal em `/consultar/`.
- Interface Pulse FX em `/consultar2/`.
- Consulta personalizada por data, entre hoje e os seis meses anteriores.
- Uso do valor final do dia retornado pela API histórica.
- Histórico JSON em `/api/historico/`.
- Gráfico dinâmico com as últimas dez consultas.
- Destaque do menor e do maior valor, incluindo a data da consulta.
- Identificação de consultas personalizadas na atividade e no gráfico.
- Tratamento de timeout, falha de rede, erro HTTP e resposta inválida.
- Django Admin para visualizar os registros salvos.

## Como executar

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra `http://127.0.0.1:8000/consultar2/`.

## Configuração segura

Copie `.env.example` para `.env` e preencha `DJANGO_SECRET_KEY` com uma chave
exclusiva do ambiente. O arquivo `.env` não deve ser enviado ao GitHub.

As URLs das APIs podem ser substituídas por `COTACAO_URL` e
`COTACAO_HISTORICO_URL`.

## Testes

```powershell
python manage.py check
python manage.py test
```

Os testes usam mocks para não depender da internet.

## Rotas

| Rota | Finalidade |
| --- | --- |
| `/` | Tela original de consulta |
| `/consultar/` | Tela original de consulta |
| `/consultar2/` | Interface Pulse FX com gráfico |
| `/api/historico/` | Histórico em JSON |
| `/admin/` | Administração dos registros |

## Segurança e versionamento

Materiais didáticos, banco local, ambientes virtuais, arquivos `.env` e
instruções internas ficam fora do versionamento. Antes de publicar, revise o
histórico do Git para garantir que nenhum segredo tenha sido incluído.

## Diagnóstico e correções

Consulte [ERROS_E_SOLUCOES.md](ERROS_E_SOLUCOES.md) para o registro das causas,
soluções e procedimentos de validação aplicados durante o desenvolvimento.
