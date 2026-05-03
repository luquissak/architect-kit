from diagrams import Diagram, Cluster
import os
import sys

# Import obrigatório conforme instruções críticas
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams.aws.storage import S3
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import Dataflow, BigQuery, DataStudio
from diagrams.onprem.client import Users

# Criação do diagrama usando graph_attr, show=False e direction="LR"
with Diagram("Arquitetura Lakehouse GCP - Ingestão S3 para BigQuery", show=False, direction="LR", graph_attr=graph_attr):

    # Camada de Origem
    with Cluster("AWS Cloud"):
        s3_source = S3("S3 Bucket\n(Eventos JSON)")

    # Camada de Ingestão e Landing
    with Cluster("GCP - Ingestão e Landing Zone"):
        gcs_landing = Storage("Cloud Storage\n(Raw Data)")

    # Camada de Processamento
    with Cluster("GCP - Processamento"):
        # Dataflow é ideal para pipelines simples ou complexos de streaming/batch (ETL)
        dataflow_job = Dataflow("Dataflow\n(Pipeline de Ingestão)")

    # Camada de Armazenamento Analítico (Lakehouse)
    with Cluster("GCP - Lakehouse"):
        bigquery_dw = BigQuery("BigQuery\n(Data Warehouse)")

    # Camada de Consumo e BI
    with Cluster("GCP - Consumo"):
        # Usamos o ícone nativo do DataStudio para representar a camada visual (Looker)
        looker_dashboard = DataStudio("Looker\n(Painel Analítico)")
        
    clientes = Users("Clientes")

    # Definição do fluxo de dados da arquitetura
    s3_source >> gcs_landing >> dataflow_job >> bigquery_dw >> looker_dashboard >> clientes

# =========================================================================
# Instruções para instalação de dependências e execução do script:
#
# 1. Instale o Graphviz no seu sistema operacional (necessário para renderizar).
# 2. Instale o pacote Python 'diagrams':
#    pip install diagrams
#
# 3. Execute este script:
#    python nome_do_arquivo.py
# =========================================================================