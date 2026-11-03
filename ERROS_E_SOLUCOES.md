# Registro de erros e soluções

## 1. Diagnóstico e causa raiz

### Rota raiz retornava 404

**O que aconteceu:** a aplicação incluía `painel.urls`, mas não havia uma rota
vazia para `/`.

**Causa raiz:** `painel/urls.py` possuía apenas as rotas de consulta e da API.

### Consulta personalizada quebrava ao ler a API histórica

**O que aconteceu:** a API em tempo real retorna um objeto JSON, enquanto o
endpoint diário pode retornar uma lista de cotações.

**Causa raiz:** o código tratava todas as respostas como dicionário e tentava
chamar `.get()` em uma lista.

### Campos da nova interface se sobrepunham

**O que aconteceu:** o botão de consulta ficava sobre o texto de orientação
sobre o intervalo permitido.

**Causa raiz:** o formulário usava espaçamento negativo e não controlava a
distância entre seus elementos.

### Menor e maior valor não refletiam a consulta personalizada

**O que aconteceu:** a consulta personalizada podia ficar fora do conjunto de
dez pontos analisados pelo gráfico.

**Causa raiz:** os registros normais eram limitados antes de garantir a
inclusão do registro personalizado.

## 2. Solução e correção do código

- A rota `path('', views.consultar_cotacao, name='inicio')` foi adicionada.
- A consulta histórica agora aceita respostas em lista e usa o último item,
  que representa o valor final retornado para o dia consultado.
- A consulta personalizada valida `DD/MM/AAAA` e restringe a data ao intervalo
  entre hoje e seis meses atrás.
- Os registros personalizados guardam `data_consulta` e
  `consulta_personalizada`.
- O gráfico reserva um ponto para a consulta personalizada mais recente e a
  posiciona na última posição.
- O formulário usa grid e espaçamento positivo entre campo, instrução,
  mensagens e botão.
- Os indicadores de menor e maior valor mostram somente a data da consulta.
- A chave fixa foi removida do código. `DJANGO_SECRET_KEY` é lida do ambiente;
  sem ela, uma chave aleatória é gerada para o desenvolvimento local.

## 3. Guia do usuário e validação

1. Instale as dependências com `pip install -r requirements.txt`.
2. Execute `python manage.py migrate`.
3. Inicie o servidor com `python manage.py runserver`.
4. Acesse `/consultar/` para a tela original ou `/consultar2/` para a
   interface Pulse FX.
5. Para uma data histórica, informe `DD/MM/AAAA` no campo personalizado.
6. Consulte `/api/historico/` para conferir os registros em JSON.
7. Execute `python manage.py check` e `python manage.py test` antes de publicar.

Validação final registrada:

```text
System check identified no issues
Ran 10 tests
OK
```

Os testes usam mocks para a API externa e incluem sucesso, timeout, erro HTTP,
resposta inválida, ordenação, método somente leitura, lista vazia e consulta
personalizada dentro e fora do intervalo permitido.
