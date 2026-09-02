from fastapi import APIRouter, HTTPException
import sqlite3
import os
from datetime import datetime

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "conecta_saude.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/{request_id}/aceitar")
async def aceitar_encaminhamento(request_id: int, dados: dict):
    """Clínica aceita o encaminhamento e agenda"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    data_agendamento = dados.get("data_agendamento")
    horario_chegada = dados.get("horario_chegada")
    orientacoes = dados.get("orientacoes", "")
    
    cur.execute("""
        UPDATE requests 
        SET status = 'aceito', 
            data_agendamento = ?, 
            horario_chegada = ?, 
            orientacoes_transporte = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (data_agendamento, horario_chegada, orientacoes, request_id))
    
    conn.commit()
    conn.close()
    
    return {"status": "aceito", "message": "Encaminhamento aceito e agendado"}

@router.post("/{request_id}/solicitar-info")
async def solicitar_informacoes(request_id: int, dados: dict):
    """Solicita informações adicionais via chat"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    mensagem = dados.get("mensagem", "")
    
    cur.execute("""
        INSERT INTO chat_messages (request_id, remetente, mensagem, created_at)
        VALUES (?, 'clinica', ?, CURRENT_TIMESTAMP)
    """, (request_id, mensagem))
    
    conn.commit()
    conn.close()
    
    return {"status": "enviado", "message": "Mensagem enviada"}

@router.get("/{request_id}/chat")
async def get_chat(request_id: int):
    """Obtém histórico de chat de uma solicitação"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM chat_messages WHERE request_id = ? ORDER BY created_at ASC", (request_id,))
    rows = cur.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
