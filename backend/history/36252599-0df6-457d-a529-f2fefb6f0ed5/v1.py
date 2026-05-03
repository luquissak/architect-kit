import os
import sys

# Importação obrigatória dos atributos do grafo
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import Dataflow, BigQuery
from diagrams.onprem.analytics import Superset
from diagrams.onprem.client import Users

# Criação do diagrama com as configurações exigidas
with Diagram("Lakehouse Architecture - AWS to GCP", show=False, direction="LR", graph_attr=graph_attr):

    # Camada de Origem na AWS
    with Cluster("AWS S3 (Source)"):
        s3_source = S3("Eventos JSON S3")

    # Camadas na Google Cloud Platform
    with Cluster("Google Cloud Platform"):
        
        # Ingestão de dados e processamento simples
        with Cluster("Camada de Ingestão"):
            ingestion_job = Dataflow("Job de Ingestão\n(Dataflow/Cloud Run)")

        # Armazenamento dos dados brutos
        with Cluster("Camada de Storage (Raw)"):
            gcs_raw = Storage("GCS (Raw Data)")

        # Padrão Lakehouse utilizando o BigQuery
        with Cluster("Camada Lakehouse"):
            bq_lakehouse = BigQuery("BigQuery\n(Data Warehouse)")

    # Camada de Visualização
    with Cluster("Consumo e Analytics"):
        # Utilizamos o ícone do Superset genericamente para representar o Looker
        looker_dashboard = Superset("Looker Dashboard")

    # Clientes finais consumindo o painel
    clientes = Users("Clientes")

    # Definição do fluxo de dados (Pipeline simples)
    # S3 -> Ingestão -> Storage Bruto -> BigQuery -> Looker -> Clientes
    s3_source >> ingestion_job >> gcs_raw >> bq_lakehouse >> looker_dashboard >> clientes

"""
Instruções para executar o código:
1. Certifique-se de ter o Graphviz instalado em seu sistema operacional.
2. Instale as dependências executando: 
   pip install diagrams
3. Salve este código em um arquivo, por exemplo: arquitetura_lakehouse.py
4. Execute o script Python: 
   python arquitetura_lakehouse.py
"""