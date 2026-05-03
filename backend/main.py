import os
import sys
import uuid
import re
import glob
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_factory import LLMFactory

load_dotenv()

app = FastAPI(title="Architect Kit Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("history", exist_ok=True)
app.mount("/history", StaticFiles(directory="history"), name="history")

class GenerateRequest(BaseModel):
    provider: str
    system_prompt: str
    user_prompt: str
    arch_id: str | None = None

class GenerateResponse(BaseModel):
    content: str
    arch_id: str
    version: int
    image_url: str
    error: str | None = None

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_diagram(request: GenerateRequest):
    try:
        arch_id = request.arch_id
        if not arch_id:
            arch_id = str(uuid.uuid4())
        
        arch_dir = os.path.join("history", arch_id)
        os.makedirs(arch_dir, exist_ok=True)
        
        existing_py = glob.glob(os.path.join(arch_dir, "v*.py"))
        version = len(existing_py) + 1
        
        provider_instance = LLMFactory.get_provider(request.provider)
        modified_system_prompt = request.system_prompt + "\n\nCRITICAL INSTRUCTION: You MUST import `graph_attr` from `common_attr` (e.g. `import sys; sys.path.append(os.path.abspath('../..')); from common_attr import graph_attr`). You MUST pass `graph_attr=graph_attr` and `show=False` to the `Diagram()` class. Example: `with Diagram('Name', show=False, graph_attr=graph_attr):`. Do not include `filename`."
        
        generated_text = provider_instance.generate_code(
            system_prompt=modified_system_prompt,
            user_prompt=request.user_prompt
        )
        
        clean_code = generated_text.replace("```python\n", "").replace("```python", "").replace("```", "").strip()
        
        if "show=False" not in clean_code:
            clean_code = re.sub(r'Diagram\((.*?)\)', r'Diagram(\1, show=False)', clean_code)
            
        py_path = os.path.join(arch_dir, f"v{version}.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
            
        try:
            subprocess.run(
                [sys.executable, f"v{version}.py"],
                cwd=arch_dir,
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.CalledProcessError as e:
            return GenerateResponse(
                content=clean_code,
                arch_id=arch_id,
                version=version,
                image_url="",
                error=f"Erro de execução:\n{e.stderr}"
            )
            
        png_files = glob.glob(os.path.join(arch_dir, "*.png"))
        if not png_files:
            return GenerateResponse(
                content=clean_code,
                arch_id=arch_id,
                version=version,
                image_url="",
                error="Nenhum arquivo .png foi gerado."
            )
            
        image_url = ""
        for png in png_files:
            basename = os.path.basename(png)
            if not re.match(r'^v\d+\.png$', basename):
                target_png = os.path.join(arch_dir, f"v{version}.png")
                if os.path.exists(target_png):
                    os.remove(target_png)
                os.rename(png, target_png)
                image_url = f"http://localhost:8000/history/{arch_id}/v{version}.png"
                break
        
        if not image_url:
            image_url = f"http://localhost:8000/history/{arch_id}/v{version}.png"
            if not os.path.exists(os.path.join(arch_dir, f"v{version}.png")):
                image_url = ""
                
        return GenerateResponse(
            content=clean_code,
            arch_id=arch_id,
            version=version,
            image_url=image_url
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
