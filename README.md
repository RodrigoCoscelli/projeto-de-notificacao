<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" />
</p>

# 🏥 Notifica AME PG

**Sistema de Gestão de Notificações de Eventos Adversos** para o **AME Praia Grande**, focado em **Qualidade e Segurança do Paciente**.

O Notifica AME PG permite que qualquer colaborador registre notificações de eventos adversos, incidentes e quase-erros (*near miss*) de forma simples — inclusive de **forma anônima** — promovendo a cultura de segurança e a melhoria contínua dos processos assistenciais.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Roadmap](#-roadmap)

---

## 🎯 Visão Geral

O **Notifica AME PG** é um sistema web criado com o auxílio da I.A para gerenciamento do ciclo de vida de notificações de eventos adversos no ambiente de ambulatório. Ele contempla:

| Etapa | Descrição |
|-------|-----------|
| **1. Notificação** | Qualquer colaborador pode registrar um evento (com ou sem anonimato) |
| **2. Triagem (NSP)** | O Núcleo de Segurança do Paciente classifica o evento e direciona ao setor responsável |
| **3. Tratativa (Setor)** | O setor notificado analisa a causa raiz e registra o plano de ação |
| **4. Encerramento** | A notificação é encerrada com toda a rastreabilidade documentada |

O sistema foi projetado para ser executado localmente (on-premise), sem necessidade de infraestrutura em nuvem, utilizando **SQLite** como banco de dados e o próprio backend para servir o frontend como arquivos estáticos.

Obs: Esse projeto foi desenvolvido com auxílio da inteligência artificial e com o meu baixo conhecimento em dev, espere por bugs, falhas e faltas de segurança que eu planejo aprender como resolver tudo conforme o projeto evolui. Sem mais, fiquem avontade para sugerir melhorias e contribuir com o que puder.

---

## ✨ Funcionalidades

### Para todos os colaboradores
- ✅ **Login seguro** com autenticação JWT (token válido por 24h)
- ✅ **Criação de notificações** com data, descrição, setor envolvido e evidências (imagem/PDF)
- ✅ **Relato anônimo** — possibilidade do setor não se identificar e a informação não ir para o banco de dados
- ✅ **Rastreamento por protocolo** — consulta pública pelo número de protocolo (ex: `AMB-A1B2C3`), sem necessidade de login
- ✅ **Dados de produto** opcionais (Material / Medicamento / Equipamento) com campos de descrição, código, fabricante, registro MS, lote/série e validade
- ✅ **Dashboard** com notificações relatadas e recebidas pelo setor
- ✅ **Configurações de perfil** — alterar username, e-mail e senha

### Para o NSP (Núcleo de Segurança do Paciente)
- ✅ **Dashboard de triagem** com fila priorizada (mais antigas primeiro)
- ✅ **Classificação completa** do evento:
  - Tipo do evento (Clínico, Não clínico, Tecnovigilância, Farmacovigilância)
  - Classificação de risco (Near miss → Óbito/Never Events)
  - Meta Internacional de Segurança do Paciente
  - Indicação de setor correto (indicação do setor correto a ser notificado)
- ✅ **Encerramento direto** com justificativa (para eventos que não demandam tratativa ou que receberam o preenchimento incorreto)
- ✅ **Gerenciamento de usuários** — criar, listar e excluir contas do sistema

### Para gestão e indicadores
- ✅ **API dedicada para Power BI** com endpoint protegido por API Key
- ✅ **Cálculo automático** de dias em aberto e timestamps de cada etapa
- ✅ **Filtros e ordenação** no dashboard (por status, busca textual, mais recentes/antigos)

---

## 🏗 Arquitetura e Tecnologias

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR (Frontend)                  │
│  HTML + CSS (TailwindCSS CDN) + JavaScript Vanilla       │
│  Páginas: Login, Dashboard, Nova Notificação, Detalhe,   │
│           Configurações                                  │
└─────────────────┬───────────────────────────────────────┘
                  │  HTTP / REST (JSON)
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI + Uvicorn)            │
│                                                         │
│  Routers:                                               │
│    /api/auth          → Login, token JWT, dados do user  │
│    /api/notificacoes  → CRUD de notificações             │
│    /api/relatorios    → Endpoint Power BI (API Key)      │
│    /api/users         → Gerenciamento de usuários (NSP)  │
│                                                         │
│  Autenticação: JWT (python-jose) + bcrypt               │
│  ORM: SQLAlchemy                                        │
│  Validação: Pydantic                                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   BANCO DE DADOS (SQLite)                │
│  Arquivo: database.db                                   │
│  Tabelas: usuarios, notificacoes                        │
└─────────────────────────────────────────────────────────┘
```

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Linguagem** | Python | 3.8+ |
| **Framework Web** | FastAPI | latest |
| **Servidor ASGI** | Uvicorn | latest |
| **ORM** | SQLAlchemy | latest |
| **Banco de Dados** | SQLite | embutido |
| **Autenticação** | JWT (`python-jose`) + bcrypt | — |
| **Validação** | Pydantic | latest |
| **Frontend** | HTML5 + JavaScript + TailwindCSS (CDN) | — |
| **Fontes** | Google Fonts (Inter, Manrope) | — |
| **Ícones** | Material Symbols Outlined | — |

---

## 📁 Estrutura do Projeto

```
projeto-de-notificacao/
│
├── backend/                    # Código-fonte do servidor
│   ├── main.py                 # Ponto de entrada da aplicação FastAPI
│   ├── database.py             # Configuração do SQLAlchemy e sessões
│   ├── models.py               # Modelos ORM (Usuario, Notificacao)
│   ├── schemas.py              # Schemas Pydantic (validação de entrada/saída)
│   ├── auth.py                 # Lógica de autenticação (JWT, bcrypt)
│   ├── seed.py                 # Script para popular o banco com dados iniciais
│   └── routers/                # Rotas organizadas por domínio
│       ├── auth.py             # Endpoints de autenticação (/api/auth)
│       ├── notificacoes.py     # Endpoints de notificações (/api/notificacoes)
│       ├── reports.py          # Endpoint Power BI (/api/relatorios)
│       └── users.py            # Endpoints de usuários (/api/users)
│
├── frontend/                   # Interface web (servida estaticamente)
│   ├── index.html              # Tela de login
│   ├── dashboard.html          # Painel principal com listagem de notificações
│   ├── nova_notificacao.html   # Formulário de criação de notificação
│   ├── detalhe.html            # Detalhes, triagem (NSP) e tratativa (setor)
│   ├── configuracoes.html      # Perfil do usuário e gerenciamento (NSP)
│   └── js/
│       └── app.js              # Utilitários JS (apiFetch, logout, config Tailwind)
│
├── uploads/                    # Evidências enviadas pelos colaboradores
├── database.db                 # Banco de dados SQLite (gerado automaticamente)
├── requirements.txt            # Dependências Python
├── run.bat                     # Script de execução rápida (Windows)
├── COMO_RODAR.md               # Guia detalhado de instalação
├── CONECTAR_POWERBI.md         # Guia de integração com Power BI
└── .gitignore
```

---

## 🗺 Roadmap

Funcionalidades planejadas para versões futuras:

- [ ] Notificações por e-mail aos setores e a NSP
- [ ] Dashboard com gráficos embarcados para insights gerenciais
- [ ] Deploy em ambiente de servidor (Docker / Cloud)

---

<p align="center">
  <sub>Desenvolvido para o <strong>AME Praia Grande</strong> — Qualidade e Segurança do Paciente</sub>
</p>
