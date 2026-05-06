from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery, Dataflow, Dataproc
from diagrams.gcp.storage import Storage
from diagrams.azure.analytics import Databricks
from diagrams.onprem.database import PostgreSQL
import os
import sys

# Importação obrigatória de atributos comuns da arquitetura corporativa
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Configuração de linhas ortogonais (limpas/90°) para design
graph_attr["splines"] = "ortho"

with Diagram("Plataforma SIPML - Hub de Dados Analiticos", show=False, direction="LR", graph_attr=graph_attr):

    # --- CAMADA 1: Origens ---
    with Cluster("Camada 1: Origens de Dados"):
        databricks = Databricks("Azure Databricks\n(Delta Lake / Refinados)")
        sildc = PostgreSQL("Analytical/Training Data\n(SILDC - Dados Sintéticos)")

    # --- CAMADA 2: Ingestão e Landing ---
    with Cluster("Camada 2: Ingestão e Landing"):
        cloud_storage = Storage("Cloud Storage\n(Raw Data / Landing)")
        bq_sandbox = BigQuery("BigQuery\n(Sandbox P&D)")

    # --- CAMADA 3: Processamento ---
    with Cluster("Camada 3: Processamento Analítico"):
        with Cluster("Motores Distribuídos (P&D / Treinamento)"):
            dataproc = Dataproc("Cloud Dataproc\n(Apache Spark)")
            dataflow = Dataflow("Cloud Dataflow\n(Apache Beam)")

    # --- CAMADA 4: Destino Analítico ---
    with Cluster("Camada 4: Destino e Disseminação"):
        bq_features = BigQuery("BigQuery\n(Repositório de Features)")

    # --- FLUXOS DE DADOS REAIS ---
    
    # Azure Databricks alimenta o BigQuery Sandbox
    databricks >> bq_sandbox
    
    # SILDC alimenta o Cloud Storage
    sildc >> cloud_storage
    
    # Cloud Storage e BigQuery Sandbox fornecem dados para processamento
    cloud_storage >> dataproc
    cloud_storage >> dataflow
    bq_sandbox >> dataproc
    bq_sandbox >> dataflow
    
    # Dataproc e Dataflow persistem features no BigQuery consolidado
    dataproc >> bq_features
    dataflow >> bq_features

    # --- ESPINHA DORSAL INVISÍVEL ---
    # Força o alinhamento em colunas estruturadas, conectando líderes de cada camada
    databricks >> Edge(style="invis") >> cloud_storage >> Edge(style="invis") >> dataproc >> Edge(style="invis") >> bq_features

    # ==========================================
    # INSTRUÇÕES PARA EXECUÇÃO:
    # 1. Instale o Graphviz no seu SO (ex: sudo apt-get install graphviz ou brew install graphviz)
    # 2. Instale as dependências Python:
    #    pip install diagrams
    # 3. Execute o script:
    #    python nome_do_arquivo.py
    # ==========================================