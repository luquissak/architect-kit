import os
import sys
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import Dataflow, BigQuery, Pubsub
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.compute import Run
from diagrams.onprem.client import Users

# Importação obrigatória dos atributos de grafo
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

with Diagram("Arquitetura GCP Lakehouse e Data Agent", show=False, direction="LR", graph_attr=graph_attr):
    
    # Usuário final
    business_user = Users("Área Usuária")

    # Camada de Origem Externa
    with Cluster("AWS Cloud - Origem"):
        s3_bucket = S3("Eventos (S3)")

    # Camada de Ingestão de Dados
    with Cluster("Ingestão (GCP)"):
        gcs_landing = GCS("Landing Zone")
        pubsub_events = Pubsub("Fila de Eventos")

    # Camada de Processamento
    with Cluster("Processamento (GCP)"):
        dataflow_etl = Dataflow("Streaming / ETL")

    # Camada de Armazenamento (Lakehouse)
    with Cluster("Storage Lakehouse (GCP)"):
        bq_lakehouse = BigQuery("BigQuery (Lakehouse)")

    # Camada de Consumo / Data Agent
    with Cluster("Consumo & IA Agent"):
        agent_app = Run("Agent Backend (Cloud Run)")
        llm_model = AIPlatform("Vertex AI (LLM)")

    # Fluxo de Ingestão e Processamento
    s3_bucket >> Edge(label="Transferência S3 -> GCS") >> gcs_landing
    gcs_landing >> Edge(label="Dispara Evento") >> pubsub_events
    pubsub_events >> Edge(label="Consumo") >> dataflow_etl
    dataflow_etl >> Edge(label="Escrita / Merge") >> bq_lakehouse

    # Fluxo de Consumo e Agente de IA
    business_user >> Edge(label="Pergunta em NL") >> agent_app
    agent_app >> Edge(label="Raciocínio / GenAI") >> llm_model
    llm_model >> Edge(label="Gera SQL") >> agent_app
    agent_app >> Edge(label="Consulta") >> bq_lakehouse

# ---------------------------------------------------------
# Comandos para instalação e execução:
# 
# 1. Instalar as dependências:
# pip install diagrams
# 
# 2. Instalar o Graphviz (Necessário para renderizar o diagrama):
# No Ubuntu/Debian: sudo apt-get install graphviz
# No macOS: brew install graphviz
# No Windows: choco install graphviz
# 
# 3. Executar o script:
# python nome_do_arquivo.py
# ---------------------------------------------------------