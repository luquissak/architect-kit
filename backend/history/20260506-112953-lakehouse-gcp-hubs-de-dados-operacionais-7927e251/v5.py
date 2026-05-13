from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import Pubsub, Dataflow, Bigquery
from diagrams.gcp.database import Spanner
from diagrams.gcp.storage import GCS
from diagrams.gcp.ml import AIPlatform
from diagrams.onprem.client import Users
import sys
import os

# Importação obrigatória dos atributos comuns (graph_attr)
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Criação do diagrama omitindo 'filename' e passando graph_attr e show=False
with Diagram("GCP Data Architecture - Spanner & BigQuery", show=False, direction="LR", graph_attr=graph_attr):

    with Cluster("Camada de Ingestão"):
        # Recebimento de eventos e processamento (ETL/ELT)
        pubsub = Pubsub("Pub/Sub\n(Mensageria)")
        dataflow = Dataflow("Dataflow\n(Stream/Batch)")

    with Cluster("Camada de Armazenamento"):
        # Storage para dados brutos e banco transacional altamente escalável
        gcs = GCS("Cloud Storage\n(Raw Data)")
        spanner = Spanner("Cloud Spanner\n(Transacional)")

    with Cluster("Camada de Processamento"):
        # Data Warehouse analítico
        bq = Bigquery("BigQuery\n(DW)")

    with Cluster("Camada de Consumo"):
        # Treinamento de IA e consumo por área de negócios
        vertex = AIPlatform("Vertex AI")
        users = Users("Analistas / BI")

    # Fluxo de ingestão de dados
    pubsub >> dataflow
    dataflow >> gcs
    dataflow >> spanner

    # Carga de dados do Data Lake para o Data Warehouse
    gcs >> bq

    # LIGAÇÃO SOLICITADA: Integração direta entre Spanner e BigQuery 
    # (Representando Federated Queries ou Datastream)
    spanner >> bq

    # Fluxo de consumo dos dados processados
    bq >> vertex
    bq >> users

    # ========================================================================
    # Instruções de Instalação e Execução:
    # 1. Instale o Graphviz no seu Sistema Operacional (ex: apt-get install graphviz)
    # 2. Instale a biblioteca Python: pip install diagrams
    # 3. Execute este script: python nome_do_arquivo.py
    # ========================================================================