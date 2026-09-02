> ⚠️ **STATUS: MVP/DEMO** - Este é um protótipo funcional para demonstração. Não é uma integração operacional com o SUS. Para uso em produção, são necessárias adaptações de segurança e governança.

# 🏥 CONECTA SC SAÚDE - CSCS

> Sistema de regulação de leitos em saúde mental integrando dados reais do SIH/SUS


---

## 📌 Sobre o Projeto

O **CSCS (Conecta Santa Catarina Saúde)** é um sistema de regulação e transparência para leitos hospitalares em saúde mental, baseado em dados reais do SIH/SUS.

### Funcionalidades

- ✅ **API REST** com autenticação JWT
- ✅ **Fila de Regulação** com busca e ordenação
- ✅ **Painel de Vagas** com 51 unidades cadastradas
- ✅ **Dashboard** com 24.910 registros de internações
- ✅ **Novos Encaminhamentos** com formulário completo
- ✅ **Análise de Dados** com estatísticas descritivas

### Dados Reais

- **24.910 internações** psiquiátricas analisadas
- **51 unidades** de saúde cadastradas (CAPS + Hospitais)
- **R$ 22,86 milhões** em gastos mapeados
- Período: 2024-2026

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.14+
- Termux ou ambiente Linux

### Instalação

```bash
git clone https://github.com/deegpnini/Conecta-SC-Saude-CSCS.git
cd Conecta-SC-Saude-CSCS
pip install -r requirements.txt
cp config/.env.example .env
./scripts/iniciar
```

### Acessos

| Serviço | URL | Credenciais |
|---------|-----|-------------|
> **Credenciais de demonstração:** `admin / admin123` (apenas para teste local)
| Frontend | http://localhost:8080/login.html | admin / admin123 |
| API Docs | http://localhost:9090/docs | - |
| Dashboard | http://localhost:5000 | - |

---

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE)

---

## 👤 Autor

**Helyton Renato Gonçalves Ronchi (Hebron)**
- GitHub: [@deegpnini](https://github.com/deegpnini)

---

**"Onde a dúvida vira investigação — e a investigação salva vidas."** 🟣💙
