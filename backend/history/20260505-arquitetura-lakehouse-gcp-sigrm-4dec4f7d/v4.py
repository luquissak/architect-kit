from diagrams import Diagram, Cluster
from diagrams.aws.integration import APIGateway
from diagrams.aws.analytics import KinesisDataFirehose, Glue, EMR, Athena, Quicksight
from diagrams.aws.storage import S3
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.client import Users
import os
import sys

# Importando atributos de grafo conforme instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Criação do diagrama sem filename, com show=False e passando graph_attr
with Diagram("Arquitetura de Dados e IA", show=False, direction="LR", graph_attr=graph_attr):
    
    # Fontes de Dados
    users = Users("Sistemas/Usuários")
    
    # Camada de Ingestão
    with Cluster("Camada de Ingestão"):
        api = APIGateway("API Gateway")
        firehose = KinesisDataFirehose("Kinesis Firehose")
        
    # Camada de Armazenamento (Data Lake)
    with Cluster("Camada de Armazenamento"):
        raw = S3("Raw Zone")
        cleansed = S3("Cleansed Zone")
        curated = S3("Curated Zone")
        
    # Camada de Processamento
    with Cluster("Camada de Processamento"):
        glue = Glue("AWS Glue (ETL)")
        emr = EMR("Amazon EMR")
        
    # Camada de Inteligência Artificial
    with Cluster("Camada de IA/ML"):
        sagemaker = Sagemaker("Modelos SageMaker")
        
    # Camada de Consumo
    with Cluster("Camada de Consumo"):
        athena = Athena("Amazon Athena")
        quicksight = Quicksight("QuickSight (BI)")

    # Fluxo de Ingestão
    users >> api >> firehose >> raw
    
    # Fluxo de Processamento e Refinamento
    raw >> glue >> cleansed
    cleansed >> emr >> curated
    
    # Fluxo de IA/ML
    cleansed >> sagemaker >> curated
    
    # Fluxo de Consumo
    curated >> athena >> quicksight

# ==============================================================================
# Instruções para instalação e execução:
# 1. Instale o Graphviz no seu sistema operacional:
#    - Linux: sudo apt-get install graphviz
#    - Mac: brew install graphviz
#    - Windows: choco install graphviz
# 2. Instale as dependências Python:
#    pip install diagrams
# 3. Certifique-se de que o arquivo 'common_attr.py' existe no caminho especificado ('../../').
# 4. Salve este código em um arquivo (ex: arquitetura.py) e execute:
#    python arquitetura.py
# ==============================================================================