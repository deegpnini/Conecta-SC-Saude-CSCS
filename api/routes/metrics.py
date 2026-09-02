from fastapi import APIRouter, Depends
from api.database import get_db_connection
from api.auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_metrics(current_user: dict = Depends(get_current_user)):
    with get_db_connection() as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM requests")
        total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE status = 'aguardando'")
        aguardando = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE status = 'regulacao'")
        regulacao = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE status = 'alocado'")
        alocado = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE status = 'internado'")
        internado = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE urgency = 'alta'")
        alta = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE urgency = 'media'")
        media = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM requests WHERE urgency = 'baixa'")
        baixa = cur.fetchone()[0]
    
    return {
        "total": total,
        "status": {
            "aguardando": aguardando,
            "regulacao": regulacao,
            "alocado": alocado,
            "internado": internado
        },
        "urgencia": {
            "alta": alta,
            "media": media,
            "baixa": baixa
        },
        "tempo_medio_espera": "4.2h (estimado)"
    }
