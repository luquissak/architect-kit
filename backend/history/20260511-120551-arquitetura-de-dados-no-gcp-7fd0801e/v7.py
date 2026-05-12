import os
import sys
from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.compute import Run
from diagrams.gcp.api import APIGateway
from diagrams.onprem.client import Users
from diagrams.gcp.storage import Storage

# Import obrigatório conforme a instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

with Diagram("Arquitetura de Agentes Conversacionais BQ", show=False, direction="LR", graph_attr=graph_attr):

    # Camada de Consumo de Dados / Usuários Finais
    with Cluster("Consumo"):
        clientes = Users("Usuários (Web/Mobile)")

    # Camada de Ingestão e Orquestração
    with Cluster("Processamento & API"):
        gateway = APIGateway("API Gateway")
        backend = Run("Orquestrador de Diálogo\n(Cloud Run)")

    # Camada de Inteligência Artificial e Dados
    with Cluster("Inteligência & Dados"):
        # Ícone do BigQuery representando os agentes conversacionais (solicitação aplicada)
        bq_agent = BigQuery("Agentes Conversacionais\n(BigQuery)")
        dados_historicos = Storage("Histórico de Interações\n(Cloud Storage)")

    # Representação do Fluxo de Dados e Interações
    clientes >> gateway >> backend
    
    # O backend consulta/interage com o BQ que atua como agente conversacional
    backend >> bq_agent
    bq_agent >> backend
    
    # Salvando os logs e histórico da conversa
    backend >> dados_historicos

# ---------------------------------------------------
# Instruções de Instalação e Execução:
# 1. Instale o Graphviz no seu sistema operacional:
#    - Linux: sudo apt-get install graphviz
#    - Mac: brew install graphviz
#    - Windows: choco install graphviz
# 2. Instale a biblioteca diagrams no seu ambiente Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_script.py
# ---------------------------------------------------