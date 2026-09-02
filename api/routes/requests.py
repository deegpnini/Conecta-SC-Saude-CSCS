from api.auth import get_current_user
from fastapi import APIRouter, HTTPException
from typing import Optional
import sqlite3
import os

router = APIRouter()

DB_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "../..", "conecta_saude.db"))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
@router.get("")
async def list_requests(
    current_user: dict = Depends(get_current_user),
    specialty: Optional[str] = None,
    urgency: Optional[str] = None,
    status: Optional[str] = None
):
    """Lista todas as solicitações com filtros opcionais."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM requests WHERE 1=1"
    params = []
    
    if specialty:
        query += " AND specialty = ?"
        params.append(specialty)
    if urgency:
        query += " AND urgency = ?"
        params.append(urgency)
    if status:
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY id ASC"
    
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@router.get("/{request_id}")
async def get_request(request_id: int):
    """Obtém detalhes de uma solicitação específica."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    return dict(row)

@router.post("/")
@router.post("")
async def create_request(request_data: dict):
    """Cria uma nova solicitação."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    fields = [
        "patient_name", "patient_cpf", "patient_phone", "specialty", "urgency",
        "region", "doctor_name", "status", "priority", "observations",
        "age", "gender", "weight", "height", "neighborhood", "comorbidities",
        "previous_internacoes", "first_internacao", "cid_principal", "cid_secundario",
        "medicamentos_atuais", "alergias", "contato_emergencia", "vinculo_caps",
        "data_ultima_alta"
    ]
    
    placeholders = ", ".join(["?" for _ in fields])
    columns = ", ".join(fields)
    
    values = [request_data.get(field) for field in fields]
    
    try:
        cur.execute(f"INSERT INTO requests ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        request_id = cur.lastrowid
        conn.close()
        
        return {"id": request_id, "message": "Solicitação criada com sucesso"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{request_id}")
async def update_request(request_id: int, request_data: dict):
    """Atualiza uma solicitação existente."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM requests WHERE id = ?", (request_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    fields = [
        "patient_name", "patient_cpf", "patient_phone", "specialty", "urgency",
        "region", "doctor_name", "status", "priority", "observations",
        "age", "gender", "weight", "height", "neighborhood", "comorbidities",
        "previous_internacoes", "first_internacao", "cid_principal", "cid_secundario",
        "medicamentos_atuais", "alergias", "contato_emergencia", "vinculo_caps",
        "data_ultima_alta"
    ]
    
    set_clause = ", ".join([f"{field} = ?" for field in fields])
    values = [request_data.get(field) for field in fields]
    values.append(request_id)
    
    try:
        cur.execute(f"UPDATE requests SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()
        
        return {"message": "Solicitação atualizada com sucesso"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{request_id}")
async def delete_request(request_id: int):
    """Remove uma solicitação."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM requests WHERE id = ?", (request_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    cur.execute("DELETE FROM requests WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Solicitação removida com sucesso"}
