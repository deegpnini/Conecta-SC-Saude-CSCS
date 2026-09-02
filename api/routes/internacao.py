from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db_connection
from api.auth import get_current_user
import json

router = APIRouter()

# Dados das instituições mapeadas pelo ARCTURUS
INSTITUICOES = {
    "publicas": [
        {
            "id": 1,
            "nome": "Instituto de Psiquiatria de Santa Catarina (IPq)",
            "cidade": "São José",
            "tipo": "Público (SUS)",
            "endereco": "Rodovia SC-401, km 4, São José/SC",
            "capacidade": "Grande porte",
            "servicos": ["Emergência 24h", "Internação", "Dependência Química"],
            "contato": "(48) 3381-0000"
        },
        {
            "id": 2,
            "nome": "CAPS II AD Criciúma",
            "cidade": "Criciúma",
            "tipo": "Público (SUS)",
            "endereco": "Rua das Rosas, 150, Criciúma/SC",
            "capacidade": "Médio porte",
            "servicos": ["Acolhimento", "Ambulatorial", "Redução de Danos"],
            "contato": "(48) 3431-0000"
        },
        {
            "id": 3,
            "nome": "CAPS Içara",
            "cidade": "Içara",
            "tipo": "Público (SUS)",
            "endereco": "Avenida Procópio Lima, 500, Bairro Cristo Rei, Içara/SC",
            "capacidade": "Médio porte",
            "servicos": ["Acolhimento", "Ambulatorial", "Grupos Terapêuticos"],
            "contato": "(48) 3632-0000"
        },
        {
            "id": 4,
            "nome": "Ambulatório de Álcool e Drogas - Içara",
            "cidade": "Içara",
            "tipo": "Público (SUS)",
            "endereco": "Avenida Procópio Lima, 500, Bairro Cristo Rei, Içara/SC",
            "capacidade": "Pequeno porte",
            "servicos": ["Grupos Terapêuticos", "Suporte Familiar"],
            "contato": "(48) 3632-0001"
        }
    ],
    "privadas": [
        {
            "id": 5,
            "nome": "Casa de Saúde Rio Maina",
            "cidade": "Criciúma",
            "tipo": "Misto (Particular/Convênio/SUS)",
            "endereco": "Rodovia Jorge Lacerda, 5000, Criciúma/SC",
            "capacidade": "Grande porte",
            "servicos": ["Internação Psiquiátrica", "Estabilização de Crises", "Longo Prazo"],
            "contato": "(48) 3432-0000"
        },
        {
            "id": 6,
            "nome": "ViV | Instituto São José",
            "cidade": "São José",
            "tipo": "Privado",
            "endereco": "Rua Antônio Ferreira, 200, São José/SC",
            "capacidade": "Médio porte",
            "servicos": ["Internação", "Hospital-Dia", "Pronto Atendimento Psiquiátrico"],
            "contato": "(48) 3382-0000"
        },
        {
            "id": 7,
            "nome": "Instituto São José",
            "cidade": "São José",
            "tipo": "Privado",
            "endereco": "Rua Antônio Ferreira, 250, São José/SC",
            "capacidade": "Médio porte",
            "servicos": ["Transtornos Psíquicos", "Dependência", "Crises Agudas"],
            "contato": "(48) 3382-0001"
        },
        {
            "id": 8,
            "nome": "Centro de Reabilitação Psicossocial Novo Amanhecer",
            "cidade": "Içara",
            "tipo": "Comunidade Terapêutica",
            "endereco": "Rodovia SC-445, km 5, Içara/SC",
            "capacidade": "Médio porte",
            "servicos": ["Reabilitação Química", "Acompanhamento 24h", "Reinserção Social"],
            "contato": "(48) 3632-0002"
        },
        {
            "id": 9,
            "nome": "Comunidade Terapêutica Feminina Deus Está Aqui",
            "cidade": "Içara",
            "tipo": "Comunidade Terapêutica",
            "endereco": "Rua Maria Rosa, 100, Içara/SC",
            "capacidade": "Pequeno porte",
            "servicos": ["Reabilitação Feminina", "Atividades Terapêuticas", "Estabilização"],
            "contato": "(48) 3632-0003"
        },
        {
            "id": 10,
            "nome": "Casa de Acolhida Manjedoura",
            "cidade": "Içara",
            "tipo": "Acolhimento",
            "endereco": "Centro, Içara/SC",
            "capacidade": "Pequeno porte",
            "servicos": ["Triagem", "Encaminhamento", "Acolhimento"],
            "contato": "(48) 3632-0004"
        }
    ]
}

# Simulação de ocupação (baseada em dados reais)
OCUPACAO = {
    "Instituto de Psiquiatria de Santa Catarina (IPq)": {"leitos": 150, "ocupados": 135, "disponiveis": 15, "ocupacao": 90},
    "Casa de Saúde Rio Maina": {"leitos": 80, "ocupados": 68, "disponiveis": 12, "ocupacao": 85},
    "ViV | Instituto São José": {"leitos": 30, "ocupados": 25, "disponiveis": 5, "ocupacao": 83.3},
    "CAPS II AD Criciúma": {"leitos": 0, "ocupados": 0, "disponiveis": 0, "ocupacao": 0},
    "CAPS Içara": {"leitos": 0, "ocupados": 0, "disponiveis": 0, "ocupacao": 0},
    "Centro de Reabilitação Psicossocial Novo Amanhecer": {"leitos": 20, "ocupados": 18, "disponiveis": 2, "ocupacao": 90},
    "Comunidade Terapêutica Feminina Deus Está Aqui": {"leitos": 15, "ocupados": 13, "disponiveis": 2, "ocupacao": 86.7},
    "Instituto São José": {"leitos": 25, "ocupados": 22, "disponiveis": 3, "ocupacao": 88},
    "Ambulatório de Álcool e Drogas - Içara": {"leitos": 0, "ocupados": 0, "disponiveis": 0, "ocupacao": 0},
    "Casa de Acolhida Manjedoura": {"leitos": 0, "ocupados": 0, "disponiveis": 0, "ocupacao": 0}
}

@router.get("/instituicoes")
async def get_instituicoes(current_user: dict = Depends(get_current_user)):
    """Retorna todas as instituições mapeadas"""
    return {
        "total": len(INSTITUICOES["publicas"]) + len(INSTITUICOES["privadas"]),
        "publicas": INSTITUICOES["publicas"],
        "privadas": INSTITUICOES["privadas"],
        "comunidades": [c for c in INSTITUICOES["privadas"] if "Comunidade" in c["tipo"] or "Acolhimento" in c["tipo"]]
    }

@router.get("/instituicoes/{tipo}")
async def get_instituicoes_por_tipo(tipo: str, current_user: dict = Depends(get_current_user)):
    """Retorna instituições por tipo (publicas, privadas, comunidades)"""
    if tipo == "publicas":
        return {"instituicoes": INSTITUICOES["publicas"]}
    elif tipo == "privadas":
        return {"instituicoes": INSTITUICOES["privadas"]}
    elif tipo == "comunidades":
        comunidades = [c for c in INSTITUICOES["privadas"] if "Comunidade" in c["tipo"] or "Acolhimento" in c["tipo"]]
        return {"instituicoes": comunidades}
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido. Use: publicas, privadas, comunidades")

@router.get("/ocupacao")
async def get_ocupacao(current_user: dict = Depends(get_current_user)):
    """Retorna a ocupação simulada de cada instituição"""
    ocupacao = []
    for nome, dados in OCUPACAO.items():
        ocupacao.append({
            "instituicao": nome,
            "leitos": dados["leitos"],
            "ocupados": dados["ocupados"],
            "disponiveis": dados["disponiveis"],
            "ocupacao_percentual": dados["ocupacao"],
            "status": "🟢 Disponível" if dados["disponiveis"] > 0 else ("🔴 Lotado" if dados["leitos"] > 0 else "⚪ Ambulatorial")
        })
    return {"ocupacao": ocupacao, "total_geral": sum([o["leitos"] for o in ocupacao])}

@router.get("/protocolos")
async def get_protocolos(current_user: dict = Depends(get_current_user)):
    """Retorna os protocolos de internação"""
    return {
        "protocolos": {
            "sus": {
                "titulo": "Fluxo de Internação SUS",
                "passos": [
                    "1. Paciente chega à UPA ou CAPS de referência",
                    "2. Médico plantonista estabiliza e avalia necessidade de internação",
                    "3. Solicitação inserida no sistema SISREG (Central de Regulação)",
                    "4. Aguarda vaga em leito psiquiátrico da região",
                    "5. Se não houver vaga, paciente é transferido para IPq em São José"
                ],
                "tempo_estimado": "24h a 72h (dependendo da disponibilidade)"
            },
            "privado": {
                "titulo": "Fluxo de Internação Privado/Convênio",
                "passos": [
                    "1. Contato direto com a instituição (Casa de Saúde Rio Maina, etc.)",
                    "2. Avaliação médica na própria instituição",
                    "3. Internação imediata (se houver vaga)",
                    "4. Acompanhamento contínuo por equipe multidisciplinar"
                ],
                "tempo_estimado": "Até 24h para captação e resgate"
            },
            "comunidade_terapeutica": {
                "titulo": "Fluxo de Comunidades Terapêuticas",
                "passos": [
                    "1. Contato com a comunidade (Novo Amanhecer, etc.)",
                    "2. Triagem e avaliação de perfil",
                    "3. Internação voluntária (ou involuntária com autorização)",
                    "4. Programa de reabilitação com atividades terapêuticas"
                ],
                "tempo_estimado": "24h a 48h"
            }
        }
    }
