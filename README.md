# Conecta SC Saúde — Protótipo de Regulação de Leitos

**Protótipo de painel de regulação de leitos em saúde mental (dados públicos agregados do SIH/SUS).**

> **Status:** MVP / Demonstração. Não é integração com o SUS e não substitui sistemas oficiais de regulação.

## Sobre o projeto

O Conecta SC Saúde é um protótipo de sistema de regulação composto por:
- **Backend:** API REST construída em **FastAPI** e **SQLite**, com autenticação JWT e módulos separados (clínicas, internações, vagas, auditoria/ledger).
- **Frontend:** 5 telas demonstrativas (HTML/JS) para visualização do fluxo de encaminhamento.

O objetivo é apoiar a visualização da distribuição de leitos e a identificação de regiões com maior demanda.

## Dados

- **Fonte:** SIH/SUS (Sistema de Informações Hospitalares do SUS) — dados públicos agregados.
- **Período:** 2024 a 2026.
- **Anonimização:** os dados utilizados são agregados públicos. Nenhum dado pessoal identificável foi incluído no repositório.

## Como executar (Ambiente local)

1. Clone o repositório e instale as dependências:
   `pip install -r requirements.txt`
2. Inicie o servidor da API:
   `python scripts/run_api.py`
3. A API estará disponível em `http://localhost:9090/api/health`.
4. Para o frontend de demonstração, sirva a pasta `conecta_demo/` em um servidor HTTP (ex: `python -m http.server 8080`).

## Tecnologias

- Python 3.12+ (FastAPI, Uvicorn, Pandas, SQLite)
- HTML5, CSS3, JavaScript

## Testes

O projeto conta com testes de fumaça para validar a API.
`pytest tests/`

## Licença

MIT License.

---
**Autor:** Helyton Ronchi ([@deegpnini](https://github.com/deegpnini))
