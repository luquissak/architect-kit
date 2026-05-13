from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import PubSub, Dataflow, Dataproc, BigQuery
from diagrams.gcp.storage import Storage
from diagrams.gcp.api import APIGateway
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.database import Spanner
import sys
import os

# Importação obrigatória dos atributos comuns (graph_attr)
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Criação do diagrama omitindo 'filename' e passando graph_attr e show=False
with Diagram("Hubs de Dados Operacionais", show=False, direction="LR", graph_attr=graph_attr):

    # CAMADA 1 (Extrema Esquerda): Origens
    with Cluster("Origens - Múltiplos Hubs de Dados Operacionais"):
        hub_stream = PubSub("Hub Operacional\n(Streaming / Eventos)")
        hub_batch = Storage("Hub Operacional\n(Arquivos / Lote)")
        hub_api = APIGateway("Hub Operacional\n(APIs / Transacional)")

    # CAMADA 2 (Centro-Esquerda): Ingestão e Landing Estágio
    with Cluster("Ingestão e Landing Estágio"):
        ingest_pubsub = PubSub("Pub/Sub\n(Ingestão Streaming)")
        ingest_storage = Storage("Cloud Storage\n(Landing / Raw Data)")

    # CAMADA 3 (Centro-Direita): Motores de Processamento (Feature Engineering)
    with Cluster("Camada de Processamento"):
        proc_dataflow = Dataflow("Cloud Dataflow\n(Apache Beam)")
        proc_dataproc = Dataproc("Cloud Dataproc\n(Apache Spark)")

    # CAMADA 4 (Extrema Direita): Destinos Operacionais e Serving
    with Cluster("Destinos Operacionais e Serving"):
        dest_spanner = Spanner("Cloud Spanner\n(Operacional)")
        dest_bq = BigQuery("BigQuery\n(Repositório de Features - Serving)")
        dest_ai = AIPlatform("Vertex AI Feature Store\n(Online Serving)")

    # =========================================================
    # FLUXOS DE CONECTIVIDADE
    # =========================================================

    # De Origens para Ingestão
    hub_stream >> ingest_pubsub
    hub_batch >> ingest_storage
    hub_api >> ingest_pubsub
    hub_api >> ingest_storage

    # De Ingestão para Processamento
    ingest_pubsub >> proc_dataflow
    ingest_storage >> proc_dataflow
    ingest_storage >> proc_dataproc

    # De Processamento para Destinos (Camada 3 para 4)
    proc_dataflow >> dest_bq
    proc_dataflow >> dest_spanner
    proc_dataflow >> dest_ai  # Dataflow enviando direto para Vertex AI
    
    proc_dataproc >> dest_bq
    proc_dataproc >> dest_ai  # Dataproc enviando direto para Vertex AI
    
    # Integrações internas na Camada Final (Bidirecional entre Spanner e BigQuery)
    dest_bq - dest_spanner

    # Espinha dorsal invisível para garantir o perfeito alinhamento vertical estruturado (LR)
    hub_batch >> Edge(style="invis") >> ingest_storage >> Edge(style="invis") >> proc_dataflow >> Edge(style="invis") >> dest_bq

    # ========================================================================
    # Instruções de Instalação e Execução:
    # 1. Instale o Graphviz no seu Sistema Operacional (ex: apt-get install graphviz)
    # 2. Instale a biblioteca Python: pip install diagrams
    # 3. Execute este script: python nome_do_arquivo.py
    # ========================================================================