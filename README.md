<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" />
</p>

# 🏥 Notifica Ambulatório

**Sistema de Gestão de Notificações de Eventos Adversos** para o **Ambulatório**, focado em **Qualidade e Segurança do Paciente**.

O Notifica Ambulatório permite que qualquer colaborador registre notificações de eventos adversos, incidentes e quase-erros (*near miss*) de forma simples — inclusive de **forma anônima** — promovendo a cultura de segurança e a melhoria contínua dos processos assistenciais.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Roadmap](#-roadmap)

---

## 🎯 Visão Geral

O **Notifica Ambulatório** é um sistema web criado com o auxílio da I.A para gerenciamento do ciclo de vida de notificações de eventos adversos no ambiente de ambulatório. Ele contempla:

| Etapa | Descrição |
|-------|-----------|
| **1. Notificação** | Qualquer colaborador pode registrar um evento (com ou sem anonimato) |
| **2. Triagem (NSP)** | O Núcleo de Segurança do Paciente classifica o evento e direciona ao setor responsável |
| **3. Tratativa (Setor)** | O setor notificado analisa a causa raiz e registra o plano de ação |
| **4. Plano de Ação 5W2H** | Se solicitado na triagem, o setor preenche um plano estruturado que passa pela aprovação do NSP |
| **5. Encerramento** | A notificação é encerrada com toda a rastreabilidade documentada |

O sistema foi projetado para ser executado localmente (on-premise), sem necessidade de infraestrutura em nuvem, utilizando **SQLite** como banco de dados e o próprio backend para servir o frontend como arquivos estáticos.

Obs: Esse projeto foi desenvolvido com auxílio da inteligência artificial e com o meu baixo conhecimento em dev, espere por bugs, falhas e faltas de segurança que eu planejo aprender como resolver tudo conforme o projeto evolui. Sem mais, fiquem avontade para sugerir melhorias e contribuir com o que puder.

---

## ✨ Funcionalidades

### Para todos os colaboradores
- ✅ **Login seguro** com autenticação JWT (token válido por 24h) — aceita usuário ou e-mail
- ✅ **Recuperação de senha** — fluxo "Esqueci minha senha" com envio de código de 6 dígitos por e-mail e redefinição segura
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
- ✅ **Plano de Ação 5W2H** — o NSP pode exigir na triagem que o setor preencha um plano estruturado (O quê, Por quê, Onde, Quando, Quem, Como, Quanto Custa), que passa por aprovação/recusa do NSP antes de ser executado e concluído pelo setor
- ✅ **Governança automatizada de prazos** — cada classificação de risco possui um prazo configurável (em dias ou horas). O sistema calcula automaticamente a data limite, bloqueia a resposta do setor quando o prazo expira e permite ao NSP desbloquear com concessão de dias extras
- ✅ **Encerramento direto** com justificativa (para eventos que não demandam tratativa ou que receberam o preenchimento incorreto)
- ✅ **Gerenciamento de usuários** — criar, listar e excluir contas do sistema
- ✅ **Configuração de setores** — criar e remover setores do sistema (com proteção ao setor NSP, que não pode ser excluído)
- ✅ **Configuração de prazos** — definir prazo padrão (dias/horas) para cada classificação de risco de evento
- ✅ **Notificações por e-mail** — e-mails automáticos enviados ao NSP (novas notificações) e aos setores (triagem realizada, análise de plano), via SMTP configurável no `.env`

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
│    /api/auth          → Login, JWT, recuperação de senha │
│    /api/notificacoes  → CRUD + triagem + plano de ação  │
│    /api/relatorios    → Endpoint Power BI (API Key)     │
│    /api/users         → Gerenciamento de usuários (NSP) │
│    /api/configuracoes → Setores e prazos por risco      │
│                                                         │
│  Serviços:                                              │
│    email_service.py   → Envio de e-mails via SMTP       │
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
│  Tabelas: usuarios, notificacoes, planos_acao,          │
│           setores, configuracoes_prazo,                  │
│           password_reset_tokens                          │
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
| **E-mail** | smtplib (SMTP/SMTP_SSL) | embutido |
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
│   ├── models.py               # Modelos ORM (Usuario, Notificacao, PlanoAcao, etc.)
│   ├── schemas.py              # Schemas Pydantic (validação de entrada/saída)
│   ├── auth.py                 # Lógica de autenticação (JWT, bcrypt)
│   ├── email_service.py        # Serviço de envio de e-mails (SMTP)
│   ├── seed.py                 # Script para popular o banco com dados iniciais
│   └── routers/                # Rotas organizadas por domínio
│       ├── auth.py             # Login, JWT, recuperação de senha (/api/auth)
│       ├── notificacoes.py     # Notificações, triagem, plano de ação (/api/notificacoes)
│       ├── reports.py          # Endpoint Power BI (/api/relatorios)
│       ├── users.py            # Gerenciamento de usuários (/api/users)
│       └── configuracoes.py    # Setores e prazos (/api/configuracoes)
│
├── frontend/                   # Interface web (servida estaticamente)
│   ├── index.html              # Tela de login + recuperação de senha
│   ├── dashboard.html          # Painel principal com listagem de notificações
│   ├── nova_notificacao.html   # Formulário de criação de notificação
│   ├── detalhe.html            # Detalhes, triagem (NSP), tratativa e plano 5W2H
│   ├── configuracoes.html      # Perfil, setores, prazos e gerenciamento (NSP)
│   └── js/
│       └── app.js              # Utilitários JS (apiFetch, logout, config Tailwind)
│
├── uploads/                    # Evidências enviadas pelos colaboradores
├── database.db                 # Banco de dados SQLite (gerado automaticamente)
├── .env                        # Variáveis de ambiente (SMTP, etc.) — não versionado
├── requirements.txt            # Dependências Python
├── run.bat                     # Script de execução rápida (Windows)
├── COMO_RODAR.md               # Guia detalhado de instalação
├── CONECTAR_POWERBI.md         # Guia de integração com Power BI
└── .gitignore
```

---

## 🗺 Roadmap

Funcionalidades planejadas para versões futuras:

- [ ] Deploy em ambiente de servidor (Docker / Cloud)
- [ ] Relatórios PDF automáticos

---

<p align="center">
  <sub>Desenvolvido para o <strong>Ambulatório</strong> — Qualidade e Segurança do Paciente</sub>
</p>
