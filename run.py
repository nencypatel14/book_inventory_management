import uvicorn
from config.config import setting

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=setting.DEBUG
    )
    