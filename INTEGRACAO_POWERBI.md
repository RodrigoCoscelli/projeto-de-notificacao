# Integração com o Power BI

Este projeto possui um endpoint dedicado e protegido para alimentar dashboards do Microsoft Power BI com os dados do sistema Notifica AME PG, sem expor informações sensíveis (como descrições completas ou dados de pacientes) e já com cálculos pré-processados (como dias em aberto).

## Detalhes do Endpoint
- **URL da API:** `http://localhost:8000/api/relatorios/powerbi` *(Lembre-se de alterar `localhost:8000` para o IP ou domínio do seu servidor em produção)*
- **Método:** `GET`
- **Autenticação:** O endpoint é protegido por uma chave de API que deve ser enviada via Header (Cabeçalho) da requisição.
  - **Chave do Header:** `x-api-key`
  - **Valor Padrão:** `ame-pg-powerbi-key`

## Passo a Passo para Conectar no Power BI Desktop

1. Abra o **Power BI Desktop**.
2. Na aba **Página Inicial** (Home), clique em **Obter Dados** (Get Data) e escolha a opção **Web**.
3. Na janela que se abrir, selecione a opção **Avançado** (Advanced) em vez de *Básico*.
4. Preencha os campos da seguinte forma:
   - **Partes da URL (URL parts):** 
     - Coloque o endereço da API: `http://localhost:8000/api/relatorios/powerbi`
   - **Parâmetros de cabeçalho de solicitação HTTP (HTTP request header parameters):**
     - No primeiro campo (à esquerda), digite o nome do cabeçalho: `x-api-key`
     - No segundo campo (à direita), cole o valor da chave: `ame-pg-powerbi-key`
5. Clique em **OK**.
6. Se o Power BI perguntar sobre como se autenticar no acesso à Web, certifique-se de que a opção selecionada na esquerda seja **Anônimo** (pois a autenticação real está sendo feita pelo nosso cabeçalho customizado) e clique em **Conectar**.
7. O Power Query Editor será aberto com os dados. O Power BI identificará que o retorno é um JSON. 
8. Clique no botão **Para a Tabela** (To Table) ou expanda a coluna `List` / `Record` para que os dados sejam formatados em colunas legíveis.
9. Faça os tratamentos de tipo de dados necessários (ex: transformar `Data Ocorrencia` em tipo Data, `Dias Aberto` em Número Inteiro, etc.).
10. Clique em **Fechar e Aplicar** e comece a criar seus gráficos!

## Dados Disponíveis
O endpoint retorna uma lista em JSON com os seguintes campos consolidados:
- `Protocolo`: O código de acompanhamento da ocorrência (ex: AMB-X8J2K).
- `Setor Notificador`: O setor de origem de quem realizou a notificação.
- `Setor Sugerido Inicial`: O setor que o notificador achou que deveria receber a ocorrência inicialmente.
- `Setor Definitivo`: O setor que foi definido pelo NSP como o real responsável pela tratativa (ou o sugerido, se ainda não triado).
- `Data Ocorrencia`: A data em que o evento adverso ocorreu (YYYY-MM-DD).
- `Tipo Evento`: A classificação do evento adverso.
- `Nivel Risco`: O risco calculado (Baixo, Médio, Alto, Crítico) ou N/A.
- `Status`: O status atual da notificação (ex: "Aguardando Triagem NSP", "Pendente no Setor", "Respondido pelo Setor").
- `Dias Aberto`: Número inteiro que calcula quantos dias a ocorrência está/esteve aberta (da criação até a resposta ou até o dia atual).
- `Data Criacao`: Data e hora do registro no sistema.
- `Data Atualizacao`: Data e hora da última movimentação/atualização da ocorrência.
- `Data Triagem NSP`: A data e hora exatas de quando o NSP realizou a triagem da notificação.
- `Data Resposta Setor`: A data e hora exatas de quando o setor notificado respondeu e encerrou a ocorrência.
- `Descricao Evento`: O texto completo da descrição do que ocorreu.
- `Justificativa Analise`: A justificativa dada pelo NSP durante a triagem/análise.
- `Tratativa Acao`: A resposta com as ações tomadas pelo setor notificado.

---
**Nota de Segurança:** Em um ambiente de produção real, é altamente recomendado que você altere o valor da chave `API_KEY_POWERBI` no arquivo `backend/routers/reports.py` para um valor seguro e longo (como um UUID ou hash) e que a comunicação seja feita sempre via **HTTPS**.
