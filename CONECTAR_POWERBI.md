# Conectando o Notifica Ambulatório ao Power BI

Este guia explica passo a passo como conectar a API de relatórios do sistema **Notifica Ambulatório** ao **Microsoft Power BI Desktop** para criar dashboards e relatórios interativos.

---

## Informações da API

| Item | Valor |
|------|-------|
| **URL do Endpoint** | `http://localhost:8000/api/relatorios/powerbi` |
| **Método HTTP** | `GET` |
| **Autenticação** | API Key via Header |
| **Header de Autenticação** | `x-api-key` |
| **Chave de Acesso** | `ame-pg-powerbi-key` |
| **Formato de Resposta** | JSON (lista de objetos) |

### Campos retornados pela API

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ID` | Número | Identificador único da notificação |
| `Protocolo` | Texto | Código de acompanhamento (ex: AMB-A1B2C3) |
| `Usuario Notificador` | Texto | Nome do usuário que criou (ou "Anônimo") |
| `Setor Notificador` | Texto | Setor de quem registrou a notificação |
| `Data Ocorrencia` | Data | Data em que o evento ocorreu (YYYY-MM-DD) |
| `Descricao Evento` | Texto | Descrição completa do evento notificado |
| `Setor Sugerido` | Texto | Setor sugerido pelo notificador |
| `Setor Definitivo` | Texto | Setor responsável definido na triagem do NSP |
| `Tipo Evento` | Texto | Evento clínico, Evento não clínico, Tecnovigilância, Farmacovigilância |
| `Classificacao Risco` | Texto | Near miss, Incidente sem dano, Evento Adverso leve/moderado/grave, Óbito/Never Events, Outros |
| `Meta Internacional` | Texto | Meta internacional de segurança do paciente relacionada |
| `Status` | Texto | Aguardando Triagem NSP, Pendente no Setor, Respondida, Encerrada |
| `Justificativa Analise` | Texto | Justificativa/análise de causa informada pelo setor |
| `Tratativa Acao` | Texto | Plano de ação/tratativa informada pelo setor |
| `Motivo Encerramento` | Texto | Motivo informado pelo NSP ao encerrar diretamente |
| `Data Criacao` | Data/Hora | Data e hora do registro da notificação |
| `Data Triagem NSP` | Data/Hora | Data e hora em que o NSP realizou a triagem |
| `Data Resposta Setor` | Data/Hora | Data e hora em que o setor notificado respondeu |
| `Data Prazo Limite` | Data/Hora | Data limite estipulada para a primeira resposta |
| `Atrasada` | Texto | Retorna "Sim" se o prazo da notificação foi ultrapassado |
| `Dias Aberto` | Número | Quantidade de dias que a notificação permaneceu/permanece em aberto |
| `Requer Plano Acao` | Texto | Retorna "Sim" se o NSP exigiu preenchimento de Plano 5W2H |
| `Produto Descricao` | Texto | Descrição do material/medicamento/equipamento |
| `Produto Codigo` | Texto | Código do produto |
| `Produto Fabricante` | Texto | Fabricante do produto |
| `Produto Registro MS` | Texto | Registro no Ministério da Saúde |
| `Produto Lote Serie` | Texto | Lote ou número de série |
| `Produto Validade` | Texto | Data de validade |
| `Plano Acao Status` | Texto | Status atual do plano de ação 5W2H |
| `Plano O que` | Texto | O que será feito (What) |
| `Plano Por que` | Texto | Por que será feito (Why) |
| `Plano Onde` | Texto | Onde será feito (Where) |
| `Plano Quando` | Texto | Quando será feito (When) |
| `Plano Quem` | Texto | Quem fará (Who) |
| `Plano Como` | Texto | Como será feito (How) |
| `Plano Quanto Custa` | Texto | Quanto custa (How much) |
| `Plano Data Aprovacao` | Data/Hora | Data e hora em que o plano foi aprovado pelo NSP |
| `Plano Data Conclusao` | Data/Hora | Data e hora em que o plano foi concluído pelo setor |

---

## Passo a Passo: Conectando no Power BI Desktop

### Pré-requisito
O servidor do Notifica Ambulatório precisa estar **rodando** para que o Power BI consiga acessar a API. Certifique-se de que o servidor esteja ativo executando:
```bash
uvicorn backend.main:app --reload
```

### Passo 1 — Abrir o Power BI Desktop
Abra o **Power BI Desktop** no seu computador.

### Passo 2 — Obter Dados da Web
1. Na tela inicial, clique em **"Obter Dados"** (ou "Get Data") na aba **Página Inicial**.
2. Na janela que abrir, selecione **"Web"** e clique em **"Conectar"**.

### Passo 3 — Configurar a Requisição (Avançado)
Na janela "Da Web", selecione a aba **"Avançado"** (não a "Básico"):

1. **Partes da URL:** No campo de URL, cole:
   ```
   http://localhost:8000/api/relatorios/powerbi
   ```

2. **Parâmetros do cabeçalho de solicitação HTTP:**
   - No campo da **esquerda** (nome do parâmetro), digite:
     ```
     x-api-key
     ```
   - No campo da **direita** (valor), digite:
     ```
     ame-pg-powerbi-key
     ```

3. Clique em **"OK"**.

### Passo 4 — Transformar os Dados (Power Query)
Ao conectar com sucesso, o **Power Query Editor** será aberto:

1. O Power BI irá reconhecer os dados como uma **Lista (List)**. Clique em **"Para Tabela"** (ou "To Table") na faixa de opções e confirme clicando em "OK".
2. Clique na **seta de expansão** (⇲) no cabeçalho da coluna para expandir todos os campos do JSON.
3. **Marque todos os campos** que deseja importar e clique em "OK".
4. Ajuste os tipos de dados das colunas:
   - `Data Ocorrencia` → **Data**
   - `Data Criacao` → **Data/Hora**
   - `Data Triagem NSP` → **Data/Hora**
   - `Data Resposta Setor` → **Data/Hora**
   - `Data Prazo Limite` → **Data/Hora**
   - `Plano Data Aprovacao` → **Data/Hora**
   - `Plano Data Conclusao` → **Data/Hora**
   - `Dias Aberto` → **Número Inteiro**
   - `ID` → **Número Inteiro**

5. Clique em **"Fechar e Aplicar"** para carregar os dados no Power BI.

### Passo 5 — Criar Relatórios
Com os dados carregados, você pode criar visualizações. Algumas sugestões:

#### Indicadores úteis (Cartões):
- **Total de Notificações** → Contagem de `Protocolo`
- **Notificações em Aberto** → Contagem filtrada onde `Status` ≠ "Respondida" e ≠ "Encerrada"
- **Média de Dias em Aberto** → Média de `Dias Aberto`
- **Encerradas pelo NSP** → Contagem onde `Motivo Encerramento` não é nulo

#### Gráficos recomendados:
| Visualização | Eixo / Categoria | Valor |
|---|---|---|
| Gráfico de Barras | `Setor Definitivo` | Contagem de `Protocolo` |
| Gráfico de Pizza | `Tipo Evento` | Contagem de `Protocolo` |
| Gráfico de Barras Empilhadas | `Classificacao Risco` | Contagem de `Protocolo` |
| Gráfico de Barras | `Meta Internacional` | Contagem de `Protocolo` |
| Gráfico de Barras | `Status` | Contagem de `Protocolo` |
| Gráfico de Linha | `Data Criacao` (por mês) | Contagem de `Protocolo` |
| Tabela completa | Todos os campos | — |

#### Métricas de tempo (usando as novas datas):
- **Tempo médio de triagem** → Diferença entre `Data Triagem NSP` e `Data Criacao`
- **Tempo médio de resposta do setor** → Diferença entre `Data Resposta Setor` e `Data Triagem NSP`
- **Tempo total de resolução** → Diferença entre `Data Resposta Setor` e `Data Criacao`

> **Dica:** Crie colunas calculadas no Power BI para essas métricas:
> ```
> Tempo Triagem (dias) = DATEDIFF([Data Criacao], [Data Triagem NSP], DAY)
> Tempo Resposta (dias) = DATEDIFF([Data Triagem NSP], [Data Resposta Setor], DAY)
> Tempo Total (dias) = DATEDIFF([Data Criacao], [Data Resposta Setor], DAY)
> ```

---

## Atualização dos Dados

### Atualização Manual
Para atualizar os dados a qualquer momento:
- Clique em **"Atualizar"** (ícone 🔄) na aba **Página Inicial** do Power BI.

### Atualização Agendada (Power BI Service)
Se você publicar o relatório no **Power BI Service** (versão online):
1. Será necessário instalar e configurar o **Power BI Gateway** no computador onde o servidor roda.
2. No Power BI Service, vá em **Configurações do Conjunto de Dados** → **Atualização Agendada**.
3. Configure a frequência desejada (ex: a cada 1 hora).

> **Nota:** A atualização agendada só funciona se o servidor da API estiver acessível pela rede. Para uso em rede local, o Power BI Gateway é obrigatório.

---

## Testando a API manualmente

Antes de conectar no Power BI, você pode testar se a API está respondendo corretamente:

### Via Navegador
Acesse a documentação interativa da API em:
```
http://localhost:8000/docs
```
Procure o endpoint `/api/relatorios/powerbi` e teste com o header `x-api-key: ame-pg-powerbi-key`.

### Via PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/relatorios/powerbi" -Headers @{"x-api-key"="ame-pg-powerbi-key"} | ConvertTo-Json
```

### Via curl (se disponível)
```bash
curl -H "x-api-key: ame-pg-powerbi-key" http://localhost:8000/api/relatorios/powerbi
```

Se retornar uma lista JSON com os dados das notificações, a API está funcionando corretamente e pronta para ser consumida pelo Power BI.

---

## Resolução de Problemas

| Problema | Solução |
|----------|---------|
| **"Não foi possível conectar"** | Verifique se o servidor está rodando (`uvicorn backend.main:app --reload`) |
| **Erro 401 - Unauthorized** | Confira se o header `x-api-key` está correto: `ame-pg-powerbi-key` |
| **Dados não aparecem** | Verifique se existem notificações cadastradas no sistema |
| **Campos vazios no Power BI** | Expanda as colunas corretamente no Power Query (Passo 4) |
| **Tipos de dados errados** | Ajuste os tipos no Power Query antes de aplicar |
| **Datas aparecem como texto** | Altere o tipo da coluna para Data/Hora no Power Query |
