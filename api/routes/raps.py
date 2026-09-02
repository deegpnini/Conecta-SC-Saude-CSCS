from datetime import datetime
from fastapi import APIRouter, Depends
from api.database import get_db_connection
from api.auth import get_current_user

router = APIRouter()

@router.get("/contatos")
async def get_raps_contatos(current_user: dict = Depends(get_current_user)):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT cnes, name, region, address, specialties, cnes_verified, is_example
            FROM clinics WHERE specialties LIKE '%Saúde Mental%'
        """)
        rows = cur.fetchall()
    
    verified = []
    examples = []
    
    for row in rows:
        clinic = {
            "cnes": row["cnes"],
            "name": row["name"],
            "region": row["region"],
            "address": row["address"],
            "specialties": row["specialties"],
            "cnes_verified": row["cnes_verified"],
            "is_example": row["is_example"]
        }
        if row["cnes_verified"]:
            verified.append(clinic)
        else:
            examples.append(clinic)
    
    return {
        "fonte": "CNES/DATASUS",
        "ultima_atualizacao": datetime.utcnow().isoformat(),
        "caps_verificados": verified,
        "exemplos": examples
    }

@router.get("/sao_ludgero/fila")
async def get_fila_sao_ludgero(current_user: dict = Depends(get_current_user)):
    return {
        "fonte": "Dados simulados para demonstração",
        "total_estimado": 600,
        "perfil": {
            "psicologia": 350,
            "psiquiatria": 150,
            "dependencia_quimica": 100
        },
        "tempo_medio_espera": "7 meses (estimativa)",
        "observacao": "Número a ser validado com a Secretaria de Saúde de São Ludgero"
    }
