from .base_skill import BaseSkill
from llm_factory import LLMFactory
import re

class SecurityAuditSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "Auditoria de Segurança"

    async def run(self, context: dict) -> dict:
        code = context.get("code", "")
        provider_name = context.get("provider", "anthropic")
        
        if not code:
            return {"status": "error", "message": "Nenhum código fornecido para auditoria."}

        system_prompt = """Você é um Engenheiro de Segurança de Nuvem sênior. 
Analise o código Python da biblioteca 'diagrams' fornecido e identifique potenciais melhorias de segurança ou riscos na arquitetura desenhada.
Foque em:
1. Criptografia de dados (at rest e in transit).
2. Isolamento de rede (sub-redes públicas vs privadas).
3. Gestão de identidade (IAM, segredos).
4. Monitoramento e logs.

Responda de forma concisa em tópicos (Bullet points). Se a arquitetura parecer segura, elogie os pontos positivos."""

        user_prompt = f"Por favor, faça uma auditoria de segurança deste código de diagrama:\n\n{code}"

        try:
            provider = LLMFactory.get_provider(provider_name)
            audit_result = provider.generate_code(system_prompt, user_prompt)
            
            return {
                "status": "success",
                "findings": audit_result
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
