from diagrams import Diagram, Cluster, Edge
import sys
import os

# Adicionando caminho para import do graph_attr conforme exigido
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Imports corretos da biblioteca diagrams
from diagrams.onprem.compute import Server
from diagrams.gcp.analytics import Dataflow, BigQuery, Dataproc, Composer, Dataprep, Looker
from diagrams.gcp.database import Spanner
from diagrams.gcp.compute import Run
from diagrams.gcp.security import Iam
from diagrams.gcp.devtools import Build
from diagrams.gcp.ml import AIPlatform

with Diagram("Arquitetura Lakehouse GCP - SIGRM Simplificado", show=False, direction="LR", graph_attr=graph_attr):
    
    # 4. Camada Base com Governança, IAM e CI/CD
    with Cluster("Camada Base & Governança"):
        # Dataprep usado para representar o Dataplex
        dataplex = Dataprep("Dataplex\n(Governança via Dataprep)")
        iam = Iam("IAM\n(Autorização)")
        cloud_build = Build("Cloud Build\n(CI/CD)")
        camada_base = [dataplex, iam, cloud_build]

    # 1. Camada On Premises (Múltiplas interfaces e sistemas internos/externos)
    with Cluster("On Premises"):
        sistemas_internos = Server("Sistemas Internos")
        sistemas_externos = Server("Sistemas Externos")
        fontes_dados = [sistemas_internos, sistemas_externos]

    # 2. Camada de Ingestão e Armazenamento
    with Cluster("Ingestão & Armazenamento"):
        with Cluster("Ingestão"):
            dataflow = Dataflow("Dataflow")
            
        with Cluster("Armazenamento"):
            bq_storage = BigQuery("BigQuery\n(Lakehouse)")
            spanner = Spanner("Spanner\n(Transacional)")
            
            # Ligação/Sincronização entre os 2 serviços de armazenamento
            bq_storage - Edge(color="brown", style="dotted", label="Sincronização") - spanner

    # 3. Camada de Processamento
    with Cluster("Processamento"):
        composer = Composer("Composer\n(Orquestração)")
        
        with Cluster("Motores de Transformação"):
            # BigQuery representando o Dataform nativo
            dataform = BigQuery("Dataform\n(SQL no BQ)")
            spark = Dataproc("Dataproc Spark\n(Python)")
            run_java = Run("Cloud Run\n(Java)")
            
            processamento = [dataform, spark, run_java]

    # 5. Camada de Consumo
    with Cluster("Consumo"):
        endpoint = Run("Cloud Run\n(Endpoint API)")
        looker = Looker("Looker\n(Dashboards)")
        # AIPlatform para representar o Vertex AI (Opcional)
        vertex_ai = AIPlatform("Vertex AI\n(ML)")

    # ---- Definição de Fluxos de Dados ----
    
    # Ingestão a partir do On-Premises
    fontes_dados >> dataflow
    
    # Persistência nos armazenamentos
    dataflow >> bq_storage
    dataflow >> spanner
    
    # Alimentação da camada de processamento
    bq_storage >> dataform
    bq_storage >> spark
    spanner >> run_java
    
    # Orquestração pelo Composer
    composer >> Edge(color="darkgreen", style="dashed", label="Orquestra") >> processamento
    
    # Disponibilização para consumo
    dataform >> looker
    spark >> vertex_ai
    run_java >> endpoint
    dataform >> endpoint
    
    # Governança atuando sobre o armazenamento principal
    camada_base - Edge(style="dotted", color="gray") - bq_storage

# ---------------------------------------------------------
# COMANDOS PARA INSTALAR DEPENDÊNCIAS E RODAR O SCRIPT:
# 
# pip install diagrams
# python nome_do_arquivo.py
# ---------------------------------------------------------