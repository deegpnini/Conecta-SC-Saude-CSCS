from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db_connection
from api.auth import get_current_user

router = APIRouter()

@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, role, region, full_name, approved FROM users ORDER BY id")
        rows = cur.fetchall()
    
    return [dict(row) for row in rows]

@router.patch("/users/{user_id}/approve")
async def approve_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET approved = 1 WHERE id = ? RETURNING id, username", (user_id,))
        result = cur.fetchone()
        conn.commit()
    
    if not result:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"message": f"Usuário {result['username']} aprovado com sucesso"}
