import os
import sys
sys.path.insert(0, os.getcwd())
from api.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Servidor rodando na porta 9090")
    uvicorn.run(app, host="0.0.0.0", port=9090, log_level="info")
