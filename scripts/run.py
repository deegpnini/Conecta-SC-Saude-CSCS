from api.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Conecta SC Saúde - CSCS iniciando...")
    print("📡 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
