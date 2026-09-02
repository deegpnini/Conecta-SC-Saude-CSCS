from fastapi import APIRouter, Depends
from api.database import get_db_connection
from api.auth import get_current_user

router = APIRouter()

@router.get("/disponiveis")
async def get_vagas_disponiveis(current_user: dict = Depends(get_current_user)):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, cnes, name, region, address, total_beds, available_beds, occupancy_rate, specialties
            FROM clinics
            WHERE available_beds > 0
            ORDER BY available_beds DESC
        """)
        rows = cur.fetchall()

    vagas = []
    for row in rows:
        vagas.append({
            "id": row["id"],
            "cnes": row["cnes"],
            "name": row["name"],
            "region": row["region"],
            "address": row["address"],
            "total_beds": row["total_beds"],
            "available_beds": row["available_beds"],
            "occupancy_rate": row["occupancy_rate"],
            "specialties": row["specialties"]
        })

    return {
        "total": len(vagas),
        "vagas": vagas,
        "mensagem": f"{len(vagas)} estabelecimentos com vagas disponíveis"
    }
