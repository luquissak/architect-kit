# Adição de Backend Python com LLM Factory

A arquitetura atual faz chamadas diretas do React (frontend) para a API da Anthropic. Para permitir a escolha dinâmica entre Anthropic e Gemini de forma segura, elegante e sem problemas de CORS, propõe-se a criação de um backend em Python utilizando o padrão **Factory**.

## Vantagens dessa Abordagem
- **Segurança**: As chaves de API (Anthropic e Gemini) ficarão guardadas apenas no backend. O navegador do usuário nunca terá acesso a elas.
- **Flexibilidade**: O padrão Factory permitirá que você adicione novos provedores (como OpenAI, Groq, etc.) no futuro com facilidade, bastando criar uma nova classe.
- **Sem problemas de CORS**: O backend se encarregará de fazer as chamadas reais às APIs externas.

## User Review Required

> [!IMPORTANT]
> Este plano fará com que o seu projeto passe a ter duas partes: um **Frontend em React (Vite)** e um **Backend em Python (FastAPI)**. Para rodar o projeto localmente, será necessário rodar o servidor frontend (`npm run dev`) e o servidor backend (ex: `uvicorn`) simultaneamente. Você está de acordo com essa arquitetura?

## Open Questions

> [!NOTE]
> Você já possui o Python instalado no seu computador para que possamos criar o ambiente virtual e rodar o backend? (Se não tiver certeza, eu posso testar executando um comando).

## Proposed Changes

---

### Backend (Python / FastAPI)

Criação de uma nova pasta `backend/` contendo:

#### [NEW] `backend/requirements.txt`
Dependências do Python: `fastapi`, `uvicorn`, `anthropic`, `google-generativeai`, `python-dotenv`, `pydantic`.

#### [NEW] `backend/.env`
Armazenará as chaves:
```
ANTHROPIC_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
```

#### [NEW] `backend/llm_factory.py`
Implementação do padrão Factory:
- Uma interface base `LLMProvider`.
- `AnthropicProvider` e `GeminiProvider` que implementam a interface.
- Uma função `LLMFactory.get_provider(name)` que retorna a instância correta com base na escolha do frontend.

#### [NEW] `backend/main.py`
O servidor FastAPI com a rota `POST /api/generate`, que:
1. Recebe o prompt e o nome do provedor escolhido (`anthropic` ou `gemini`).
2. Chama a Factory para obter o provedor adequado.
3. Executa a geração de código e retorna para o frontend.

---

### Frontend (React / Vite)

#### [MODIFY] `src/App.jsx`
- Adição de um controle (como um *dropdown* ou botões de rádio) na interface para permitir a escolha entre **Claude 3.5 Sonnet (Anthropic)** ou **Gemini 1.5 (Google)**.
- Alteração da função `generate()` para não fazer mais o *fetch* diretamente para a API da Anthropic, mas sim para o nosso novo backend local (`http://localhost:8000/api/generate`), enviando os dados da arquitetura e o provedor escolhido.

#### [MODIFY] `vite.config.js`
- Atualização do proxy para apontar `/api` para o backend Python local (`http://localhost:8000`) ao invés da API externa.

#### [MODIFY] `.gitignore`
- Adicionar o diretório `backend/venv/`, a pasta `__pycache__/` e garantir que o `backend/.env` não seja rastreado.

## Verification Plan

### Automated/Manual Tests
- Instalar as dependências do backend.
- Iniciar o servidor FastAPI na porta 8000.
- Garantir que o Vite está rodando na porta 5173.
- Escolher a opção "Gemini" na interface, preencher a arquitetura e testar a geração. O diagrama em Python deve ser gerado corretamente.
- Escolher a opção "Anthropic" na interface e verificar se o sistema reclama corretamente sobre a falta de saldo (ou funciona caso os créditos sejam adicionados).
