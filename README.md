# Conecta SC Saúde — Protótipo de Regulação de Leitos

**Protótipo de painel de regulação de leitos em saúde mental (dados públicos agregados do SIH/SUS).**

> **Status:** MVP / Demonstração. Não é integração com o SUS e não substitui sistemas oficiais de regulação.

---

## Sobre o projeto

O Conecta SC Saúde é um protótipo de painel (HTML/JS) que consolida dados públicos de internações psiquiátricas do Sistema de Informações Hospitalares do SUS (SIH/SUS), entre 2024 e 2026.

O objetivo é apoiar a visualização da distribuição de leitos e a identificação de regiões com maior demanda, servindo como base para futuras discussões sobre regulação.

---

## Dados

- **Fonte:** SIH/SUS (Sistema de Informações Hospitalares do SUS) — dados públicos agregados.
- **Período:** 2024 a 2026.
- **Volume:** 24.910 registros de internações psiquiátricas.
- **Anonimização:** os dados utilizados são apenas agregados públicos. Nenhum dado pessoal identificável (nome, CPF, CNS, endereço) foi incluído ou gerado no repositório.

---

## O que o protótipo mostra

- Total de internações psiquiátricas no período.
- Valor total associado às internações (R$ 22,86 milhões).
- Distribuição por unidade hospitalar (51 unidades).
- Distribuição por região de saúde.
- Painel de vagas (simulado com base nas internações históricas).

---

## Como executar

O protótipo é um único arquivo HTML/JS estático.

1. Abra o arquivo `index.html` no navegador:
   - Duplo clique no arquivo local, ou
   - `python3 -m http.server 8000` na pasta do projeto e acesse `http://localhost:8000`.
2. Os dados estão embutidos no HTML (não há backend).

---

## Tecnologias

- HTML5, CSS3, JavaScript (puro).
- Dados extraídos e agregados do SIH/SUS via scripts Python (não inclusos neste repositório).

---

## Limitações

- **Protótipo de demonstração.** Não é sistema oficial de regulação.
- Não integra com sistemas do SUS.
- Dados agregados de 2024–2026 (não tempo real).
- Painel de vagas é simulado com base em internações históricas.

---

## Licença

MIT License.

---

**Autor:** Helyton Ronchi ([@deegpnini](https://github.com/deegpnini))
