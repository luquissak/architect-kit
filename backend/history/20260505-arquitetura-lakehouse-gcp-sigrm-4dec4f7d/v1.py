from diagrams import Diagram, Cluster, Edge
import sys
import os

# Adicionando caminho para import do graph_attr conforme exigido
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Imports da biblioteca diagrams para os provedores solicitados
from diagrams.onprem.compute import Server
from diagrams.gcp.analytics import Dataflow, BigQuery, Dataproc, Composer, Dataplex, Looker
from diagrams.gcp.database import Spanner
from diagrams.gcp.compute import Run
from diagrams.gcp.security import Iam
from diagrams.gcp.devtools import Build
from diagrams.gcp.ml import AIPlatform

with Diagram("Arquitetura Lakehouse GCP - SIGRM", show=False, direction="LR", graph_attr=graph_attr):
    
    # 4. Camada Base com Governança, IAM e CI/CD
    with Cluster("Camada Base & Governança"):
        dataplex = Dataplex("Dataplex\n(Governança)")
        iam = Iam("IAM\n(Autorização)")
        cloud_build = Build("Cloud Build\n(CI/CD)")
        camada_base = [dataplex, iam, cloud_build]

    # 1. Camada On Premises (Sistemas Internos/Externos)
    with Cluster("On Premises"):
        sistemas = [
            Server("Sistemas Internos"),
            Server("Sistemas Externos")
        ]

    # 2. Camada de Ingestão e Armazenamento
    with Cluster("Ingestão & Armazenamento"):
        dataflow = Dataflow("Dataflow\n(Ingestão)")
        
        with Cluster("Storage"):
            bq_storage = BigQuery("BigQuery\n(Lakehouse)")
            spanner = Spanner("Spanner\n(Transacional)")
            
            # Ligação direta entre os serviços de armazenamento
            bq_storage - Edge(color="brown", style="dotted", label="Sincronização") - spanner

    # 3. Camada de Processamento
    with Cluster("Processamento"):
        composer = Composer("Composer\n(Orquestração)")
        
        with Cluster("Transformação e Lógica"):
            # Usando ícone do BigQuery para representar o Dataform nativo
            dataform = BigQuery("Dataform\n(SQL)")
            spark = Dataproc("Dataproc Spark\n(Python)")
            run_java = Run("Cloud Run\n(Java)")
            
            processamento = [dataform, spark, run_java]

    # 5. Camada de Consumo
    with Cluster("Consumo"):
        endpoint = Run("Cloud Run\n(Endpoint API)")
        looker = Looker("Looker\n(BI / Dashboards)")
        # Usando AIPlatform genérico para representar Vertex AI com segurança de versão
        vertex_ai = AIPlatform("Vertex AI\n(ML / IA)")

    # ---- Definição de Fluxo de Dados ----
    
    # Extração das fontes On-Premises para Ingestão
    sistemas >> dataflow
    
    # Ingestão persistindo no Storage
    dataflow >> bq_storage
    dataflow >> spanner
    
    # Leitura do Storage para a camada de Processamento
    bq_storage >> dataform
    bq_storage >> spark
    spanner >> run_java
    
    # Composer orquestrando as rotinas de processamento
    composer >> Edge(color="darkgreen", style="dashed", label="Orquestra") >> processamento
    
    # Resultados do Processamento servidos para Consumo
    dataform >> looker
    spark >> vertex_ai
    run_java >> endpoint
    dataform >> endpoint
    
    # Ligação representativa da camada de governança cruzando a arquitetura
    camada_base - Edge(style="dotted", color="gray") - bq_storage

    # ---------------------------------------------------------
    # COMANDOS PARA INSTALAR DEPENDÊNCIAS E RODAR O SCRIPT:
    # 
    # pip install diagrams
    # python nome_do_arquivo.py
    # ---------------------------------------------------------