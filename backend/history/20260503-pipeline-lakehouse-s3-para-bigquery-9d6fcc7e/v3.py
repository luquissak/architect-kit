from diagrams import Diagram, Cluster, Edge
import sys
import os

# Importação obrigatória de atributos comuns conforme instruções críticas
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams.aws.storage import S3
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import Dataflow, BigQuery, Looker
from diagrams.onprem.client import User

# Instanciação do Diagrama com as regras definidas
with Diagram("Pipeline Lakehouse - S3 para BigQuery com Looker", show=False, direction="LR", graph_attr=graph_attr):

    # Camada de Origem na AWS
    with Cluster("Fonte de Dados (AWS)"):
        s3_bucket = S3("Bucket S3\n(Arquivos JSON)")

    # Camadas do Lakehouse no GCP
    with Cluster("Google Cloud Platform - Lakehouse"):
        
        # Camada de Ingestão / Landing
        with Cluster("Camada Raw (Ingestão)"):
            gcs_landing = Storage("Cloud Storage\n(Landing Zone)")
            
        # Camada de Processamento / ETL
        with Cluster("Camada de Processamento"):
            dataflow_etl = Dataflow("Dataflow\n(Processamento Batch)")
            
        # Camada de Armazenamento / Serving
        with Cluster("Camada Serving"):
            bigquery_dw = BigQuery("BigQuery\n(Data Warehouse)")
            
        # Camada de Consumo / BI
        with Cluster("Camada de Consumo"):
            looker_bi = Looker("Looker\n(Dashboards)")

    # Usuário final consumindo os dados
    business_user = User("Usuários de Negócio")

    # Definição do fluxo de dados com setas e comentários
    # 1. Transferência do S3 para o GCS (Ex: via Storage Transfer Service)
    s3_bucket >> Edge(label="Storage Transfer\nService", color="darkorange") >> gcs_landing
    
    # 2. Leitura dos dados brutos JSON no Cloud Storage pelo Dataflow
    gcs_landing >> Edge(label="Lê JSON", color="blue") >> dataflow_etl
    
    # 3. Escrita dos dados estruturados no BigQuery
    dataflow_etl >> Edge(label="Grava Tabelas\n(Estruturado)", color="forestgreen") >> bigquery_dw
    
    # 4. Looker consome dados do BigQuery para montar os Dashboards
    bigquery_dw >> Edge(label="Consulta Dados", color="purple") >> looker_bi
    
    # 5. Usuário acessa os Dashboards no Looker
    looker_bi >> Edge(label="Visualiza Dashboards", color="darkblue") >> business_user

# =====================================================================
# INSTRUÇÕES PARA INSTALAÇÃO E EXECUÇÃO
# =====================================================================
# 1. Instale o Graphviz no seu sistema operacional:
#    - Linux (Debian/Ubuntu): sudo apt-get install graphviz
#    - MacOS: brew install graphviz
#    - Windows: winget install graphviz ou choco install graphviz
#
# 2. Instale a biblioteca Python 'diagrams':
#    pip install diagrams
#
# 3. Execute o script:
#    python nome_do_arquivo.py
# =====================================================================