import os
import sys
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery, Dataflow, Dataproc, Pubsub
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform
from diagrams.onprem.database import PostgreSQL, MySQL
from diagrams.onprem.queue import Kafka

# Ajuste para garantir conexões ortogonais, conforme exigido pela arquitetura
graph_attr["splines"] = "ortho"

with Diagram("Plataforma SIPML - Camada de Ingestao e Processamento", show=False, direction="LR", graph_attr=graph_attr):
    
    # --- COLUNA 1: Origens de Dados e Eventos ---
    with Cluster("Origens de Dados e Eventos"):
        
        with Cluster("Hubs de Dados Analíticos (Múltiplos)"):
            hub_analitico_a = PostgreSQL("Hub Analítico A")
            hub_analitico_b = MySQL("Hub Analítico B")
            hubs_analiticos = [hub_analitico_a, hub_analitico_b]
            
        with Cluster("Hubs de Dados Operacionais (Múltiplos)"):
            hub_op_streaming = Kafka("Hub Operacional A\n(Streaming)")
            hub_op_bases = PostgreSQL("Hub Operacional B\n(Bases/APIs)")

    # --- COLUNA 2: Camada de Ingestão e Armazenamento Raw ---
    with Cluster("Camada de Ingestão e Armazenamento Raw"):
        pubsub = Pubsub("Pub/Sub\n(Mensageria)")
        cloud_storage = Storage("Cloud Storage\n(Landing/Raw Data)")

    # --- COLUNA 3: Camada de Processamento e Feature Engineering ---
    with Cluster("Camada de Processamento e Feature Engineering"):
        with Cluster("Motores de Processamento Distribuído"):
            dataflow = Dataflow("Dataflow\n(Streaming/Batch)")
            dataproc = Dataproc("Dataproc\n(Batch/Spark)")

    # --- COLUNA 4: Destinos Analíticos e Feature Store ---
    with Cluster("Destinos Analíticos e Feature Store"):
        bigquery = BigQuery("BigQuery\n(Repositório de Features)")
        vertex_ai = AIPlatform("Vertex AI\n(Feature Store)")

    # --- FLUXOS DE DADOS ---
    
    # Hubs Analíticos -> Lote direto para Cloud Storage
    hubs_analiticos >> cloud_storage
    
    # Hubs Operacionais -> Streaming para Pub/Sub e tabelas para Storage
    hub_op_streaming >> pubsub
    hub_op_bases >> cloud_storage
    
    # Cloud Storage -> Processamento Batch
    cloud_storage >> dataflow
    cloud_storage >> dataproc
    
    # Pub/Sub -> Processamento Streaming
    pubsub >> dataflow
    
    # Processamento -> Destino Analítico Central (BigQuery)
    dataflow >> bigquery
    dataproc >> bigquery
    
    # BigQuery -> Vertex AI Feature Store
    bigquery >> vertex_ai

    # --- ESPINHA DORSAL INVISÍVEL PARA ALINHAMENTO VERTICAL ---
    # Força a estruturação das colunas perfeitamente da esquerda para a direita
    hub_analitico_a >> Edge(style="invis") >> cloud_storage >> Edge(style="invis") >> dataproc >> Edge(style="invis") >> bigquery

# ==========================================
# INSTRUÇÕES PARA EXECUÇÃO:
# 1. Instale o Graphviz no seu SO (ex: sudo apt-get install graphviz ou brew install graphviz)
# 2. Instale as dependências Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_arquivo.py
# ==========================================