from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import time
import os

app = FastAPI(title="CSCS API", version="2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.getenv("DATABASE_PATH", "./conecta_saude.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/health")
async def health():
    return {"status": "online", "timestamp": time.time()}

@app.get("/api/clinicas")
async def list_clinicas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clinicas")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/requests")
async def list_requests():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================================
# ROTA DE DETALHES - CORRIGIDA
# ============================================================
@app.get("/api/requests/{request_id}")
async def get_request(request_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    return dict(row)

@app.post("/api/auth/login")
async def login(request: dict):
    username = request.get("username")
    password = request.get("password")
    
    if username == "admin" and password == "admin123":
        return {"access_token": "fake-token", "token_type": "bearer", "role": "admin"}
    
    return {"erro": "Credenciais inválidas"}

@app.on_event("startup")
async def startup():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clinicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cnes TEXT, cidade TEXT,
            leitos INTEGER, vagas INTEGER, ocupacao INTEGER, tipo_leito TEXT
        )
    ''')
    
    cur.execute("SELECT COUNT(*) FROM clinicas")
    if cur.fetchone()[0] == 0:
        clinicas = [
            ("Casa de Saúde Rio Maina", "RI0003", "Criciúma", 80, 12, 85, "Psiquiatria Geral"),
            ("CAPS II Tubarão", "2661365", "Tubarão", 80, 0, 100, "Saúde Mental"),
            ("Hospital São José", "2706369", "Criciúma", 120, 3, 97, "Psiquiatria Geral"),
            ("CAPS III", "2522209", "Criciúma", 60, 8, 86, "Saúde Mental"),
            ("Hospital Regional", "2436450", "Araranguá", 100, 2, 98, "Psiquiatria Geral"),
            ("CAPS AD", "2302101", "Tubarão", 40, 5, 87, "Álcool e Drogas"),
        ]
        cur.executemany('''
            INSERT INTO clinicas (nome, cnes, cidade, leitos, vagas, ocupacao, tipo_leito)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', clinicas)
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT, patient_cpf TEXT, patient_phone TEXT,
            specialty TEXT, urgency TEXT, region TEXT, doctor_name TEXT,
            status TEXT, priority TEXT, observations TEXT,
            age INTEGER, gender TEXT, cid_principal TEXT, vinculo_caps TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🚀 Banco inicializado")

print("🚀 Servidor rodando na porta 9090")
