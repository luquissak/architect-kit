from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import BigQuery
from diagrams.onprem.client import Client, Users
import os
import sys

# Import obrigatório do common_attr conforme instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

with Diagram("Arquitetura Executiva - Lakehouse GCP", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada de Origem de Dados (AWS)
    with Cluster("Origem"):
        # Fonte dos eventos em JSON
        s3_bucket = S3("AWS S3\n(Eventos JSON)")

    # Camada de Ingestão de Dados (GCP)
    with Cluster("Ingestão"):
        # Pipe simples representando o landing dos dados na GCP
        landing_zone = GCS("Cloud Storage\n(Landing Zone)")

    # Camada de Processamento e Armazenamento (Lakehouse)
    with Cluster("Processamento & Armazenamento"):
        # BigQuery atuando como Data Warehouse/Lakehouse
        lakehouse_bq = BigQuery("BigQuery\n(Lakehouse)")

    # Camada de Consumo e Visualização
    with Cluster("Consumo"):
        # Representação do Painel Looker para consumo
        looker_dash = Client("Painel Looker")
        # Clientes finais consumindo o painel
        clientes = Users("Clientes Finais")

    # Definição do fluxo de dados (Pipeline executivo)
    s3_bucket >> landing_zone >> lakehouse_bq >> looker_dash >> clientes

    # ========================================================================
    # INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
    # 1. Instale o Graphviz no seu SO (https://graphviz.org/download/)
    # 2. Instale a biblioteca Python: pip install diagrams
    # 3. Execute este script no terminal: python nome_do_script.py
    # ========================================================================