from diagrams import Diagram, Cluster
import sys
import os

# Importando atributos comuns obrigatórios
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Imports corretos da biblioteca diagrams para os provedores mencionados
from diagrams.aws.storage import S3
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import Dataflow, BigQuery
from diagrams.onprem.client import Users

# Garantindo o fallback visual (ícone de dashboard/monitoramento) caso o nó Looker não exista nativamente
try:
    from diagrams.gcp.analytics import Looker
except ImportError:
    try:
        from diagrams.saas.analytics import Looker
    except ImportError:
        from diagrams.gcp.operations import Monitoring as Looker

# Criando o diagrama com show=False, graph_attr obrigatório e direção LR
with Diagram("GCP Lakehouse Architecture", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada de Origem: Dados residem inicialmente na AWS S3
    with Cluster("AWS Cloud"):
        s3_source = S3("Eventos JSON")

    # Arquitetura Cloud no GCP (Padrão Lakehouse)
    with Cluster("Google Cloud Platform (GCP)"):
        
        # Camada de Ingestão: Bucket de aterrissagem dos dados vindos do S3
        with Cluster("Ingestão"):
            gcs_landing = GCS("Cloud Storage\n(Raw Landing)")
            
        # Camada de Processamento: Job para leitura, transformação e carga dos JSONs
        with Cluster("Processamento"):
            dataflow_etl = Dataflow("Dataflow\n(ETL / Transformação)")
            
        # Camada de Armazenamento: Data Warehouse gerenciado agindo como Lakehouse
        with Cluster("Armazenamento"):
            bigquery_lakehouse = BigQuery("BigQuery\n(Lakehouse)")
            
        # Camada de Consumo: Visualização de dados para o usuário final
        with Cluster("Consumo"):
            # Substituição realizada: O nó Looker agora representa o painel de BI
            looker_panel = Looker("Looker\n(Painel de BI)")

    # Atores: Clientes consumindo o dashboard final
    clientes = Users("Clientes")

    # Fluxo de dados (Pipeline)
    s3_source >> gcs_landing >> dataflow_etl >> bigquery_lakehouse >> looker_panel >> clientes

"""
# Instruções para instalação das dependências e execução do script:
# 1. Instale o Graphviz no seu sistema operacional (necessário para a biblioteca diagrams).
# 2. Instale as bibliotecas Python:
#    pip install diagrams
# 3. Execute este script:
#    python nome_do_arquivo.py
"""