from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.gcp.analytics import Bigquery, Dataflow
from diagrams.gcp.storage import GCS
from diagrams.onprem.client import Users
import os
import sys

# Import obrigatório do graph_attr para customização e padronização do diagrama
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# ------------------------------------------------------------------------
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
# 1. Instale o motor do Graphviz no SO (ex: sudo apt-get install graphviz)
# 2. Instale o pacote Python diagrams: pip install diagrams
# 3. Execute o script via terminal: python nome_do_arquivo.py
# ------------------------------------------------------------------------

# Definição do Diagrama (omitindo filename, usando show=False, direction="LR" e graph_attr)
with Diagram("Arquitetura Lakehouse GCP", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada 1: Origem de Dados hospedada na AWS
    with Cluster("Camada de Origem"):
        eventos_s3 = S3("Eventos JSON\n(AWS S3)")
        
    # Camada 2: Ingestão e Processamento na nuvem destino (GCP)
    with Cluster("Camada de Ingestão"):
        # Dataflow é utilizado aqui como um pipeline simples para coleta e transformação dos dados
        pipe_ingestao = Dataflow("Pipe de Ingestão\n(Cloud Dataflow)")
        
    # Camada 3: Armazenamento e estruturação do Lakehouse
    with Cluster("Camada Lakehouse (GCP)"):
        # GCS serve de landing zone (área raw) temporária ou permanente
        landing_zone = GCS("Landing Zone\n(Cloud Storage)")
        # BigQuery estrutura os dados servindo como motor analítico central
        bq_lakehouse = Bigquery("DW / Lakehouse\n(BigQuery)")
        
    # Camada 4: Consumo e visualização dos dados pelos clientes
    with Cluster("Camada de Consumo"):
        # Representação do acesso dos clientes finais ao dashboard do Looker
        looker_dash = Users("Painel Looker\n(Clientes)")
        
    # Definição do fluxo de dados (Pipeline)
    eventos_s3 >> pipe_ingestao >> landing_zone >> bq_lakehouse >> looker_dash