from fastapi import APIRouter
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "conecta_saude.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
@router.get("/todas")
async def list_clinicas():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Verificar se a tabela existe
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clinicas'")
    if not cur.fetchone():
        conn.close()
        # Dados mockados baseados nos prints que você tinha
        return [
            {"id": 1, "nome": "Casa de Saúde Rio Maina", "cnes": "RI0003", "cidade": "Criciúma", "leitos": 80, "vagas": 12, "ocupacao": 85},
            {"id": 2, "nome": "CAPS II Tubarão", "cnes": "2661365", "cidade": "Tubarão", "leitos": 80, "vagas": 0, "ocupacao": 100},
            {"id": 3, "nome": "Bem Viver Centro de Saúde", "cnes": "BEM004", "cidade": "Camboriú", "leitos": 20, "vagas": 3, "ocupacao": 85},
            {"id": 4, "nome": "Clínica Psiquiátrica Garcia", "cnes": "GAR006", "cidade": "Criciúma", "leitos": 15, "vagas": 2, "ocupacao": 87},
            {"id": 5, "nome": "Novo Amanhecer", "cnes": "NOV010", "cidade": "Içara", "leitos": 20, "vagas": 2, "ocupacao": 90},
            {"id": 6, "nome": "Clínica Reabilitação Dependentes", "cnes": "CLI012", "cidade": "Balneário Camboriú", "leitos": 25, "vagas": 4, "ocupacao": 84},
            {"id": 7, "nome": "Complexo Santo Agostinho", "cnes": "SAN008", "cidade": "Criciúma", "leitos": 25, "vagas": 4, "ocupacao": 84},
            {"id": 8, "nome": "Comunidade Emanuel", "cnes": "EMA016", "cidade": "Içara", "leitos": 15, "vagas": 1, "ocupacao": 93},
            {"id": 9, "nome": "Recanto da Esperança", "cnes": "REC014", "cidade": "Florianópolis", "leitos": 18, "vagas": 2, "ocupacao": 89},
            {"id": 10, "nome": "Comunidade Pradda", "cnes": "PRA015", "cidade": "Içara", "leitos": 15, "vagas": 2, "ocupacao": 87},
            {"id": 11, "nome": "Comunidade Renascer", "cnes": "REN013", "cidade": "Gravataí", "leitos": 20, "vagas": 2, "ocupacao": 90},
            {"id": 12, "nome": "Hospital Nossa Senhora Conceição", "cnes": "NON009", "cidade": "Urussanga", "leitos": 40, "vagas": 7, "ocupacao": 83},
            {"id": 13, "nome": "Hospital Custódia Psiquiátrica", "cnes": "HOSP007", "cidade": "Florianópolis", "leitos": 40, "vagas": 5, "ocupacao": 88},
            {"id": 14, "nome": "Instituto Neurociências", "cnes": "INJ005", "cidade": "Criciúma", "leitos": 0, "vagas": 0, "ocupacao": 100},
            {"id": 15, "nome": "VIV Instituto São José", "cnes": "VIV002", "cidade": "São José", "leitos": 30, "vagas": 5, "ocupacao": 83}
        ]
    
    cur.execute("SELECT * FROM clinicas")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
