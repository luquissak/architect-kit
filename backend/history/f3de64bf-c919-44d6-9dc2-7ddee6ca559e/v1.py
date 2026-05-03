import sys
import os
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import Dataflow, BigQuery, Looker
from diagrams.onprem.client import Users

# Criação do Diagrama da Arquitetura Lakehouse na GCP
with Diagram("GCP Lakehouse Architecture", show=False, direction="LR", graph_attr=graph_attr):

    # Camada de Origem: AWS
    with Cluster("AWS Cloud"):
        s3_source = S3("S3 Bucket\n(Eventos JSON)")

    # Nuvem de Destino: Google Cloud Platform
    with Cluster("Google Cloud Platform (Lakehouse)"):
        
        # Camada de Ingestão
        with Cluster("Ingestão"):
            gcs_staging = GCS("Cloud Storage\n(Staging Area)")

        # Camada de Processamento
        with Cluster("Processamento"):
            dataflow_etl = Dataflow("Dataflow\n(ETL / Parser JSON)")

        # Camada de Armazenamento / Lakehouse
        with Cluster("Armazenamento"):
            bigquery = BigQuery("BigQuery\n(Data Warehouse)")

        # Camada de Consumo
        with Cluster("Consumo & Analytics"):
            looker = Looker("Looker\n(Dashboards)")

    # Entidade Externa: Clientes
    clientes = Users("Clientes")

    # Definição do fluxo de dados
    # S3 envia eventos JSON para o GCS na GCP
    # Dataflow processa os arquivos do GCS e insere as tabelas estruturadas no BigQuery
    # Looker consome dados do BigQuery para montar os painéis
    # Clientes visualizam o painel final no Looker
    s3_source >> gcs_staging >> dataflow_etl >> bigquery >> looker >> clientes

"""
# Instruções para instalação e execução:
# 1. Certifique-se de ter o Graphviz instalado em seu sistema operacional.
# 2. Instale a biblioteca diagrams:
#    pip install diagrams
# 3. Salve este código em um arquivo chamado 'diagrama_lakehouse.py'
# 4. Execute o script via terminal:
#    python diagrama_lakehouse.py
"""