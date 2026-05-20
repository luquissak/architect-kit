import os
import sys
import uuid
import re
import glob
import subprocess
import datetime
import unicodedata
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

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def load_diagram_mappings():
    mappings = {}
    # Procurar no diretório backend ou na raiz
    mapping_file = "diagram_mappings.md"
    if not os.path.exists(mapping_file):
        mapping_file = os.path.join(os.path.dirname(__file__), "diagram_mappings.md")
        
    if os.path.exists(mapping_file):
        with open(mapping_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Padrão para extrair das tabelas MD: | `de` | ... | `para` |
            matches = re.findall(r'\| `(.*?)` \|.*?\| `(.*?)` \|', content)
            for original, alternative in matches:
                mappings[original.strip()] = alternative.strip().replace('\\n', '\n')
    return mappings


def apply_diagram_fixes(py_path, error_message):
    mappings = load_diagram_mappings()
    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    # Tentar substituições de caminhos completos ou parciais
    for original, alternative in mappings.items():
        # Se o erro cita o nome que temos mapeado
        if original in content and (original in error_message or original.split('.')[-1] in error_message):
            content = content.replace(original, alternative)
            modified = True
        
        # Caso o mapeamento seja no formato provedor.classe (ex: onprem.database.SQLServer)
        elif "." in original:
            parts = original.split(".")
            class_name = parts[-1]
            module_path = ".".join(parts[:-1])
            if class_name in error_message and module_path in error_message:
                # Tenta substituir a linha de import ou a classe
                # Ex: from diagrams.onprem.database import SQLServer -> from diagrams.azure.database import SQLDatabases
                old_import = f"from diagrams.{module_path} import {class_name}"
                new_parts = alternative.split(".")
                new_class = new_parts[-1]
                new_module = ".".join(new_parts[:-1])
                new_import = f"from diagrams.{new_module} import {new_class} as {class_name}"
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    modified = True

    if modified:
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(content)
    return modified

from skills.security_audit_skill import SecurityAuditSkill

class GenerateRequest(BaseModel):
    provider: str
    system_prompt: str
    user_prompt: str
    arch_id: str | None = None
    run_audit: bool = False

class GenerateResponse(BaseModel):
    content: str
    arch_id: str
    version: int
    image_url: str
    error: str | None = None
    audit_report: str | None = None
    log: str | None = None

@app.get("/api/history")
async def list_history():
    history_dir = "history"
    entries = []
    if not os.path.exists(history_dir):
        return entries
        
    for arch_id in os.listdir(history_dir):
        arch_path = os.path.join(history_dir, arch_id)
        if os.path.isdir(arch_path):
            # Tentar extrair informações do log.md ou dos arquivos v*.py
            name = arch_id
            date = ""
            
            log_path = os.path.join(arch_path, "log.md")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    first_line = f.readline()
                    # Ex: ## Versão 1 - 2026-05-03 19:56:26
                    match = re.search(r'Versão \d+ - (.*)', first_line)
                    if match:
                        date = match.group(1)
            
            entries.append({
                "id": arch_id,
                "name": name,
                "date": date
            })
            
    # Ordenar por data (assumindo que o ID começa com data YYYYMMDD)
    entries.sort(key=lambda x: x["id"], reverse=True)
    return entries

@app.get("/api/history/{arch_id}")
async def get_history_detail(arch_id: str):
    arch_dir = os.path.join("history", arch_id)
    if not os.path.exists(arch_dir):
        raise HTTPException(status_code=404, detail="Arquitetura não encontrada")
        
    existing_py = glob.glob(os.path.join(arch_dir, "v*.py"))
    if not existing_py:
        raise HTTPException(status_code=404, detail="Nenhum código encontrado")
        
    # Pegar a versão mais recente
    versions = []
    for f in existing_py:
        match = re.search(r'v(\d+)\.py', os.path.basename(f))
        if match:
            versions.append(int(match.group(1)))
    
    latest_version = max(versions)
    py_path = os.path.join(arch_dir, f"v{latest_version}.py")
    
    with open(py_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    image_url = f"http://localhost:8000/history/{arch_id}/v{latest_version}.png"
    if not os.path.exists(os.path.join(arch_dir, f"v{latest_version}.png")):
        image_url = ""
        
    log_path = os.path.join(arch_dir, "log.md")
    log_content = ""
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
            
    return {
        "arch_id": arch_id,
        "version": latest_version,
        "content": code,
        "image_url": image_url,
        "log": log_content
    }

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_diagram(request: GenerateRequest):
    try:
        provider_instance = LLMFactory.get_provider(request.provider)
        modified_system_prompt = request.system_prompt + "\n\nCRITICAL INSTRUCTION: You MUST import `graph_attr` from `common_attr` (e.g. `import sys; sys.path.append(os.path.abspath('../..')); from common_attr import graph_attr`). You MUST pass `graph_attr=graph_attr` and `show=False` to the `Diagram()` class. Example: `with Diagram('Name', show=False, graph_attr=graph_attr):`. Do not include `filename`."
        
        generated_text = provider_instance.generate_code(
            system_prompt=modified_system_prompt,
            user_prompt=request.user_prompt
        )
        
        clean_code = generated_text.replace("```python\n", "").replace("```python", "").replace("```", "").strip()
        
        if "show=False" not in clean_code:
            clean_code = re.sub(r'Diagram\((.*?)\)', r'Diagram(\1, show=False)', clean_code)
            
        arch_id = request.arch_id
        if not arch_id:
            # Extrair título do Diagrama para compor o nome da pasta
            title_match = re.search(r'Diagram\([\'"]([^\'"]+)[\'"]', clean_code)
            title = title_match.group(1) if title_match else "arquitetura"
            datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            unique_suffix = str(uuid.uuid4())[:8]
            arch_id = f"{datetime_str}-{slugify(title)}-{unique_suffix}"
        
        arch_dir = os.path.join("history", arch_id)
        os.makedirs(arch_dir, exist_ok=True)
        
        existing_py = glob.glob(os.path.join(arch_dir, "v*.py"))
        version = len(existing_py) + 1
        
        py_path = os.path.join(arch_dir, f"v{version}.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
            
        # Salvar Log
        log_path = os.path.join(arch_dir, "log.md")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"## Versão {version} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Prompt do Usuário:**\n{request.user_prompt}\n\n")
            f.write("---\n")
            
        try:
            # Primeira tentativa de execução
            subprocess.run(
                [sys.executable, f"v{version}.py"],
                cwd=arch_dir,
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.CalledProcessError as e:
            # Tentar aplicar correções automáticas
            if apply_diagram_fixes(py_path, e.stderr):
                try:
                    # Segunda tentativa após fix
                    subprocess.run(
                        [sys.executable, f"v{version}.py"],
                        cwd=arch_dir,
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                except subprocess.CalledProcessError as e2:
                    return GenerateResponse(
                        content=clean_code,
                        arch_id=arch_id,
                        version=version,
                        image_url="",
                        error=f"Erro após tentativa de correção automática:\n{e2.stderr}"
                    )
            else:
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
                
        audit_report = None
        if request.run_audit:
            audit_skill = SecurityAuditSkill()
            audit_result = await audit_skill.run({
                "code": clean_code,
                "provider": request.provider
            })
            if audit_result["status"] == "success":
                audit_report = audit_result["findings"]

        # Ler Log atualizado
        current_log = ""
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                current_log = f.read()

        return GenerateResponse(
            content=clean_code,
            arch_id=arch_id,
            version=version,
            image_url=image_url,
            audit_report=audit_report,
            log=current_log
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

