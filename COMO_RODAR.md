# Como Rodar o Projeto: Notifica AME PG

Este projeto é composto por um backend construído em **FastAPI** (Python) e um frontend em **HTML/CSS/JavaScript puro** que é servido estaticamente pelo próprio backend.

## Pré-requisitos

- **Python 3.8+** instalado na sua máquina.

---

## ⚠️ IMPORTANTE: Por Que o Projeto Pode Não Rodar

O erro mais comum é o `ModuleNotFoundError: No module named 'fastapi'` (ou outro pacote).

**Causa**: O ambiente virtual (`venv`) existe na pasta, mas os pacotes **não foram instalados dentro dele**.

Isso acontece quando:
- Você clonou/copiou o projeto para uma máquina nova.
- O `venv` foi recriado ou apagado.
- As dependências foram instaladas em outro Python (global), e não dentro do `venv`.

**Solução**: Sempre que isso acontecer, execute o Passo 2 abaixo para reinstalar as dependências.

---

## Passo a Passo

### 1. Preparando o Ambiente (Opcional, mas recomendado)
Abra o terminal na pasta raiz do projeto e crie um ambiente virtual:

No Windows (PowerShell/CMD):
```bash
python -m venv venv
```

> Se a pasta `venv` já existir, pule este passo.

### 2. ✅ Instalação das Dependências (OBRIGATÓRIO em nova máquina ou após recriar o venv)
Com o terminal aberto na pasta do projeto, instale os pacotes:

```bash
.\venv\Scripts\pip.exe install -r requirements.txt
```

> **Dica**: Use `.\venv\Scripts\pip.exe` diretamente (sem precisar "ativar" o ambiente) para garantir que os pacotes sejam instalados no lugar certo.

### 3. (Opcional) Popular o Banco de Dados
Se for a primeira vez rodando o projeto ou se você precisar resetar o banco de dados e inserir os usuários padrões (admin_nsp, farmacia, recepcao, enfermagem), rode o script de seed:

```bash
.\venv\Scripts\python.exe -m backend.seed
```

### 4. Iniciando o Servidor
Para iniciar a aplicação, utilize o Uvicorn dentro do ambiente virtual:

```bash
.\venv\Scripts\uvicorn.exe backend.main:app --reload
```

*A flag `--reload` faz com que o servidor reinicie automaticamente sempre que você salvar alguma alteração no código.*

> **Alternativa**: Você também pode dar um duplo clique no arquivo `run.bat` na pasta do projeto — ele faz tudo automaticamente.

### 5. Acessando a Aplicação
Com o servidor rodando, abra o seu navegador de preferência e acesse:

- **Aplicação (Frontend)**: [http://localhost:8000/](http://localhost:8000/)
- **Documentação Automática da API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Contas de Acesso Padrão (Criadas pelo Seed)

Se você rodou o passo 3, poderá entrar no sistema utilizando qualquer uma das contas abaixo. Todas possuem a senha **`senha123`**:

- **Usuário:** `admin_nsp` (Setor: NSP - Possui acesso completo de triagem)
- **Usuário:** `farmacia` (Setor: Farmácia)
- **Usuário:** `recepcao` (Setor: Recepção)
- **Usuário:** `enfermagem` (Setor: Enfermagem)

---

## Solução de Problemas

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: No module named 'fastapi'` | Dependências não instaladas no venv | Execute o Passo 2 |
| `uvicorn` não é reconhecido | Usando o Python global em vez do venv | Use `.\venv\Scripts\uvicorn.exe` |
| Porta 8000 já em uso | Outro servidor rodando | Feche o outro servidor ou use `--port 8001` |
| Erro de senha/login | Banco não populado | Execute o Passo 3 (seed) |
