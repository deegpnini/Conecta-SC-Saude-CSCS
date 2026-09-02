import hashlib
import json
from fastapi import APIRouter, Depends
from api.database import get_db_connection
from api.auth import get_current_user

router = APIRouter()

def compute_hash(event_type: str, event_data: dict, previous_hash: str) -> str:
    content = json.dumps({
        "event_type": event_type,
        "event_data": event_data,
        "previous_hash": previous_hash
    }, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

def add_ledger_event(event_type: str, event_data: dict) -> dict:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT hash FROM event_ledger ORDER BY id DESC LIMIT 1")
        last = cur.fetchone()
        previous_hash = last["hash"] if last else "0" * 64
        
        block_hash = compute_hash(event_type, event_data, previous_hash)
        
        cur.execute("""
            INSERT INTO event_ledger (event_type, event_data, previous_hash, hash)
            VALUES (?, ?, ?, ?)
            RETURNING id, event_type, event_data, previous_hash, hash, created_at
        """, (event_type, json.dumps(event_data), previous_hash, block_hash))
        
        result = cur.fetchone()
        conn.commit()
        
        return {
            "id": result["id"],
            "event_type": result["event_type"],
            "event_data": json.loads(result["event_data"]),
            "previous_hash": result["previous_hash"],
            "hash": result["hash"],
            "created_at": result["created_at"]
        }

@router.get("/verify")
async def verify_ledger(current_user: dict = Depends(get_current_user)):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM event_ledger")
        total_blocks = cur.fetchone()[0]
        
        if total_blocks == 0:
            return {"valid": True, "blocks": 0, "hash": "0"*64, "message": "Ledger vazio"}
        
        cur.execute("SELECT id, event_type, event_data, previous_hash, hash, created_at FROM event_ledger ORDER BY id")
        blocks = cur.fetchall()
    
    valid = True
    for i, block in enumerate(blocks):
        event_data = json.loads(block["event_data"])
        expected_hash = compute_hash(block["event_type"], event_data, block["previous_hash"])
        if expected_hash != block["hash"]:
            valid = False
            break
        if i > 0:
            prev_hash = blocks[i-1]["hash"]
            if block["previous_hash"] != prev_hash:
                valid = False
                break
    
    current_hash = blocks[-1]["hash"] if valid else "0"*64
    
    return {
        "valid": valid,
        "blocks": total_blocks,
        "hash": current_hash,
        "message": "Cadeia criptográfica íntegra" if valid else "Cadeia comprometida"
    }
