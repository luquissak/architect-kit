import os
import sys
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import Bigquery, Dataflow
from diagrams.saas.analytics import Looker
from diagrams.onprem.client import Users

# =====================================================================
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
# 1. Instale o Graphviz no seu SO (dependência do diagrams):
#    - Ubuntu/Debian: sudo apt-get install graphviz
#    - MacOS: brew install graphviz
#    - Windows: choco install graphviz
# 2. Instale a biblioteca Python:
#    pip install diagrams
# 3. Execute este script:
#    python nome_do_arquivo.py
# =====================================================================

with Diagram("GCP Lakehouse Architecture", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada de Origem na AWS
    with Cluster("AWS Environment"):
        s3_source = S3("S3 Bucket\n(JSON Events)")

    # Ambiente GCP centralizando a arquitetura Lakehouse
    with Cluster("GCP - Lakehouse Platform"):
        
        # Camada de Ingestão e Landing Zone
        with Cluster("1. Ingestion & Landing"):
            # O Dataflow representa o "pipe simples" extraindo do S3
            ingestion_pipe = Dataflow("Dataflow\n(Ingestion Pipe)")
            # Storage recebendo os arquivos raw como staging
            gcs_raw = Storage("Cloud Storage\n(Raw JSON)")
        
        # Camada de Processamento e Armazenamento (Lakehouse)
        with Cluster("2. Processing & Storage"):
            # BigQuery atuando como Lakehouse central
            bq_lakehouse = Bigquery("BigQuery\n(Data Warehouse / Lakehouse)")
        
        # Camada de Consumo e Visualização
        with Cluster("3. Consumption"):
            # Looker consumindo dados tratados do BQ
            looker_dash = Looker("Looker\n(Dashboards)")
    
    # Usuários finais acessando os painéis
    clients = Users("Clients")

    # Definição do fluxo de dados
    s3_source >> ingestion_pipe >> gcs_raw >> bq_lakehouse >> looker_dash >> clients