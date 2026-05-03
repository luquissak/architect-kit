import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_factory import LLMFactory

# Carrega as variáveis do arquivo .env no backend
load_dotenv()

app = FastAPI(title="Architect Kit Backend")

# Configurar CORS (embora no React via Vite proxy não seja estritamente necessário, é uma boa prática)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    provider: str
    system_prompt: str
    user_prompt: str

class GenerateResponse(BaseModel):
    content: str

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_diagram(request: GenerateRequest):
    try:
        provider_instance = LLMFactory.get_provider(request.provider)
        generated_text = provider_instance.generate_code(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt
        )
        return GenerateResponse(content=generated_text)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
