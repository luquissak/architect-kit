from diagrams import Diagram, Cluster, Edge
import sys
import os

# Instrução crítica: Importar graph_attr do arquivo common_attr
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Definindo atributos globais para o fluxo em spline ortogonal
graph_attr["splines"] = "ortho"

# Importações corretas dos módulos GCP corrigidas para evitar ImportError
from diagrams.gcp.analytics import PubSub, Dataflow, Dataproc, BigQuery
from diagrams.gcp.storage import Storage
from diagrams.gcp.api import APIGateway
from diagrams.gcp.ml import AIPlatform

# Criação do Diagrama da Arquitetura focada nos Hubs Operacionais
with Diagram("Lakehouse GCP - Hubs de Dados Operacionais", show=False, direction="LR", graph_attr=graph_attr):
    
    # CAMADA 1: Origens / Múltiplos Hubs
    with Cluster("Origens - Múltiplos Hubs de Dados Operacionais"):
        hub_stream = PubSub("Hub Operacional\n(Streaming / Eventos)")
        hub_batch = Storage("Hub Operacional\n(Arquivos / Lote)")
        hub_api = APIGateway("Hub Operacional\n(APIs / Transacional)")
        
    # CAMADA 2: Ingestão e Área de Pouso (Landing)
    with Cluster("Ingestão e Landing Estágio"):
        ingest_pubsub = PubSub("Pub/Sub\n(Ingestão Streaming)")
        ingest_gcs = Storage("Cloud Storage\n(Landing / Raw Data)")
        
    # CAMADA 3: Motores de Processamento (Feature Engineering)
    with Cluster("Camada de Processamento"):
        proc_dataflow = Dataflow("Cloud Dataflow\n(Apache Beam)")
        proc_dataproc = Dataproc("Cloud Dataproc\n(Apache Spark)")
        
    # CAMADA 4: Destinos Operacionais e Serving
    with Cluster("Destinos Operacionais e Serving"):
        dest_bq = BigQuery("BigQuery\n(Repositório de Features - Serving)")
        dest_vertex = AIPlatform("Vertex AI Feature Store\n(Online Serving)")
        
    # ==========================================
    # FLUXOS DE DADOS E CONECTIVIDADE
    # ==========================================
    
    # 1. Fluxo de Ingestão: Origens -> Hubs Temporários (Landing/Mensageria)
    hub_stream >> ingest_pubsub
    hub_batch >> ingest_gcs
    hub_api >> ingest_pubsub
    hub_api >> ingest_gcs
    
    # 2. Fluxo de Processamento: Landing/Mensageria -> Motores (Dataflow/Dataproc)
    ingest_pubsub >> proc_dataflow
    ingest_gcs >> proc_dataflow
    ingest_gcs >> proc_dataproc
    
    # 3. Fluxo de Armazenamento Final: Motores -> BigQuery
    proc_dataflow >> dest_bq
    proc_dataproc >> dest_bq
    
    # 4. Fluxo de Consumo/Serving: BigQuery -> Vertex AI Feature Store
    dest_bq >> dest_vertex
    
    # ==========================================
    # ESPINHA DORSAL INVISÍVEL
    # ==========================================
    # Assegura o alinhamento vertical das colunas forçando o desenho da esquerda para a direita
    hub_stream >> Edge(style="invis") >> ingest_pubsub >> Edge(style="invis") >> proc_dataflow >> Edge(style="invis") >> dest_bq

# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
# 1. Crie um ambiente virtual e instale a biblioteca: `pip install diagrams`
# 2. Instale o motor Graphviz no seu sistema (necessário para a renderização):
#    - Ubuntu/Debian: `sudo apt install graphviz`
#    - macOS: `brew install graphviz`
#    - Windows: `winget install graphviz` ou baixe o executável do site oficial
# 3. Certifique-se de que a raiz do seu projeto possua o `common_attr.py` válido
# 4. Execute o script: `python nome_do_script.py`
# ==============================================================================