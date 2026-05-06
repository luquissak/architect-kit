import os
import sys

# Importação do graph_attr conforme instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Forçando conexões ortogonais conforme as especificações
graph_attr["splines"] = "ortho"

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import PubSub, Dataflow, Dataproc, BigQuery
from diagrams.gcp.storage import Storage
from diagrams.gcp.network import APIGateway
from diagrams.gcp.ml import AIPlatform

# Criação do Diagrama da Arquitetura Lakehouse GCP
with Diagram("Lakehouse GCP - Hubs de Dados Operacionais", show=False, direction="LR", graph_attr=graph_attr):
    
    # CAMADA 1: Origens / Hubs Operacionais
    with Cluster("Origens - Múltiplos Hubs de Dados Operacionais"):
        hub_stream = PubSub("Hub Operacional\n(Streaming / Eventos)")
        hub_batch = Storage("Hub Operacional\n(Arquivos / Lote)")
        hub_api = APIGateway("Hub Operacional\n(APIs / Transacional)")
        
    # CAMADA 2: Ingestão e Área de Pouso (Landing)
    with Cluster("Ingestão e Landing"):
        ingest_pubsub = PubSub("Pub/Sub\n(Ingestão Streaming)")
        ingest_gcs = Storage("Cloud Storage\n(Landing / Raw Data)")
        
    # CAMADA 3: Processamento e Engenharia de Features
    with Cluster("Camada de Processamento"):
        proc_dataflow = Dataflow("Cloud Dataflow\n(Apache Beam)")
        proc_dataproc = Dataproc("Cloud Dataproc\n(Apache Spark)")
        
    # CAMADA 4: Destinos / Consumo Operacional
    with Cluster("Destinos Operacionais e Serving"):
        dest_bq = BigQuery("BigQuery\n(Repositório de Features)")
        dest_vertex = AIPlatform("Vertex AI Feature Store\n(Online Serving)")
        
    # ==========================================
    # MAPEAMENTO DE FLUXOS E CONECTIVIDADE
    # ==========================================
    
    # 1. Ingestão: Origens -> Landing/Mensageria
    hub_stream >> ingest_pubsub
    hub_batch >> ingest_gcs
    hub_api >> ingest_pubsub
    hub_api >> ingest_gcs
    
    # 2. Processamento: Landing/Mensageria -> Motores (Dataflow / Dataproc)
    ingest_pubsub >> proc_dataflow
    ingest_gcs >> proc_dataflow
    ingest_gcs >> proc_dataproc
    
    # 3. Armazenamento Final: Motores -> BigQuery
    proc_dataflow >> dest_bq
    proc_dataproc >> dest_bq
    
    # 4. Serving: BigQuery -> Vertex AI
    dest_bq >> dest_vertex
    
    # ==========================================
    # ESPINHA DORSAL INVISÍVEL
    # ==========================================
    # Garante o alinhamento vertical rigoroso das colunas da esquerda para a direita
    hub_stream >> Edge(style="invis") >> ingest_pubsub >> Edge(style="invis") >> proc_dataflow >> Edge(style="invis") >> dest_bq

# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
# 1. Instale a biblioteca diagrams: `pip install diagrams`
# 2. Instale o motor Graphviz no seu sistema operacional:
#    - Linux (Ubuntu/Debian): `sudo apt install graphviz`
#    - macOS: `brew install graphviz`
#    - Windows: `winget install graphviz` ou baixe o instalador oficial
# 3. Certifique-se de ter o arquivo `common_attr.py` acessível no caminho configurado.
# 4. Execute o script: `python nome_do_script.py`
# ==============================================================================