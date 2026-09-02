from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from api.database import get_db_connection
from api.auth import hash_password, verify_password, create_jwt_token, get_current_user

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    region: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.post("/register")
async def register(user: UserCreate):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (user.username, user.email))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Usuário ou e-mail já cadastrado")
        
        password_hash = hash_password(user.password)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, role, region, full_name, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            RETURNING id, username, email, role, region, full_name
        """, (user.username, user.email, password_hash, "medico", user.region, user.full_name, 0))
        result = cur.fetchone()
        conn.commit()
    
    return {
        "message": "Usuário registrado. Aguardando aprovação do administrador.",
        "user": {
            "id": result["id"],
            "username": result["username"],
            "email": result["email"],
            "role": result["role"],
            "region": result["region"],
            "full_name": result["full_name"]
        }
    }

@router.post("/login")
async def login(user: UserLogin):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, email, password_hash, role, region, full_name, approved
            FROM users WHERE username = ?
        """, (user.username,))
        db_user = cur.fetchone()
    
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    if not db_user["approved"] and db_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Usuário aguardando aprovação")
    
    token = create_jwt_token(db_user["id"], db_user["username"], db_user["role"])
    
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 86400,
        "user": {
            "id": db_user["id"],
            "username": db_user["username"],
            "email": db_user["email"],
            "role": db_user["role"],
            "region": db_user["region"],
            "full_name": db_user["full_name"]
        }
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    token = create_jwt_token(current_user["id"], current_user["username"], current_user["role"])
    return {"access_token": token, "token_type": "Bearer", "expires_in": 86400}

@router.post("/change-password")
async def change_password(request: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE id = ?", (current_user["id"],))
        user = cur.fetchone()
        
        if not user or not verify_password(request.current_password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Senha atual incorreta")
        
        new_hash = hash_password(request.new_password)
        cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user["id"]))
        conn.commit()
    
    return {"message": "Senha alterada com sucesso"}
