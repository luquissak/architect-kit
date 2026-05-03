from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.analytics import BigQuery, Dataflow, Datastudio
from diagrams.onprem.client import Users
import sys
import os

# Import obrigatório conforme instruções críticas
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Inicialização do diagrama com as configurações exigidas
with Diagram("GCP Lakehouse Architecture", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada de Origem de Dados: Armazenamento externo na AWS
    with Cluster("AWS - Source"):
        s3_events = S3("Eventos JSON\n(S3 Bucket)")
        
    # Camada de Ingestão: Pipeline simples para mover os dados
    with Cluster("GCP - Ingestion"):
        ingestion_pipe = Dataflow("Pipe Simples\n(Dataflow)")
        
    # Camada de Armazenamento/Processamento: Padrão Lakehouse no GCP
    with Cluster("GCP - Storage & Compute"):
        lakehouse = BigQuery("Lakehouse\n(BigQuery)")
        
    # Camada de Consumo: Visualização e acesso aos dados
    with Cluster("Consumption"):
        dashboard = Datastudio("Painel\n(Looker)")
        clients = Users("Clientes")

    # Definição do fluxo de dados da arquitetura
    s3_events >> ingestion_pipe >> lakehouse >> dashboard >> clients

    # ---------------------------------------------------------
    # Dependências e Execução:
    # 1. Instale o Graphviz no seu sistema (ex: brew install graphviz ou apt-get install graphviz)
    # 2. Instale a biblioteca Python: pip install diagrams
    # 3. Execute o script: python nome_do_arquivo.py
    # ---------------------------------------------------------