# Implementação do Backend com LLM Factory concluída!

Nesta etapa, adicionamos uma camada de **Backend em Python (FastAPI)** para remover do frontend a responsabilidade de lidar com as chamadas de IA. Isso aumentou muito a segurança do projeto e nos permitiu implementar o Padrão de Projeto **Factory**, que nos possibilita escolher dinamicamente qual Inteligência Artificial vai gerar os diagramas.

## O que foi alterado:

### 1. Novo Backend Python
- Criamos a pasta `backend/` com a estrutura completa para uma aplicação FastAPI.
- Arquivos importantes criados:
  - `llm_factory.py`: O "cérebro" que gerencia qual IA chamar. Ele tem as classes `AnthropicProvider` e `GeminiProvider`.
  - `main.py`: O servidor que expõe a rota `POST /api/generate`.
  - `.env`: Para armazenar a `ANTHROPIC_API_KEY` e a futura `GEMINI_API_KEY`.
  - `requirements.txt`: Com as dependências necessárias (`fastapi`, `uvicorn`, `anthropic`, `google-generativeai`).

### 2. Frontend React Atualizado
- Modificamos o `src/App.jsx` para adicionar um seletor visual na interface ("Motor de IA") onde é possível escolher entre **Claude 3.5** e **Gemini 1.5**.
- Removemos a chamada direta (e as gambiarras de CORS) para a Anthropic. Agora o React chama nosso backend local `POST /api/generate`.

### 3. Configurações
- Alteramos o `vite.config.js` para redirecionar todas as chamadas `/api/*` do Vite para o nosso servidor FastAPI que vai rodar na porta 8000.
- Atualizamos o `.gitignore` para proteger suas chaves do backend.

---

> [!CAUTION]
> **Ação Necessária: Instalar o Python!**
> 
> Durante a inicialização automática do backend, notei que **o Python não está instalado** no seu sistema Windows (ou não está configurado no PATH).
> 
> Para que o projeto completo funcione, siga os passos abaixo:
> 1. Baixe o Python no site oficial: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
> 2. Durante a instalação, marque a caixa **"Add python.exe to PATH"** (Isso é muito importante!).
> 3. Após instalar, abra um novo terminal na pasta `backend` do projeto e execute:
>    ```bash
>    python -m venv venv
>    .\venv\Scripts\activate
>    pip install -r requirements.txt
>    uvicorn main:app --reload
>    ```
> 
> Se o seu React não estiver mais rodando, abra outro terminal na raiz do projeto e rode `npm run dev`.

Quando o Python estiver instalado e o servidor FastAPI rodando, você poderá colocar a sua chave do Gemini no arquivo `backend/.env` e testar a geração usando a API gratuita do Google!
