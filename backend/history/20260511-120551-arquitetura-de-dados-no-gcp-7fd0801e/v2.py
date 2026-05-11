from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import SQLDatabases
from diagrams.onprem.compute import Server
from diagrams.gcp.network import VPN
from diagrams.gcp.analytics import Composer, Dataproc, BigQuery, DataCatalog, DataStudio
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import ComputeEngine
from diagrams.onprem.analytics import Jupyter
from diagrams.onprem.client import Users, Client

import sys
import os

# Configuração de atributos globais (Import Obrigatório)
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Diretriz: LINHAS ORTOGONAIS
# Forçando o roteamento ortogonal para evitar efeito "teia de aranha" com ângulos de 90 graus.
graph_attr["splines"] = "ortho"

# Criação do Diagrama 
# Diretriz: DIREÇÃO LR (Left to Right)
with Diagram("Arquitetura de Dados no GCP", show=False, direction="LR", graph_attr=graph_attr):

    # -----------------------------------------------------------
    # ISOLAMENTO LÓGICO DAS CAMADAS EM COLUNAS
    # -----------------------------------------------------------

    with Cluster("Camada 1: Origens de Dados"):
        # Representando fontes isoladas
        sql_server = SQLDatabases("SQL Server")
        sap_bw = Server("SAP BW")
        
    with Cluster("Camada 2: Conectividade e Ingestão"):
        # Gateway de VPN, Orquestração e Ingestão
        vpn = VPN("VPN Gateway")
        airflow = Composer("Airflow\n(Cloud Composer)")
        gcs = Storage("Cloud Storage\n(Landing Zone)")
        pyspark_ingest = Dataproc("PySpark Ingestão\n(Dataproc Serverless)")
        
    with Cluster("Camada 3: Pipeline e Processamento de Dados"):
        # Ferramentas de Transformação e Processamento (Computação)
        bq_pipelines = BigQuery("BigQuery Pipelines\n(BQ Studio)")
        runtime = ComputeEngine("Runtime Engine")
        spark_proc = Dataproc("Spark\n(Dataproc)")
        notebook = Jupyter("Notebook\n(Colab/BQ)")
        sql_script = BigQuery("Script SQL\n(BQ Studio)")
        
    with Cluster("Camada 4: Armazenamento Analítico (Medalhão)"):
        # Arquitetura Medalhão centralizada
        bq_bronze = BigQuery("BigQuery Bronze\n(Dados Brutos)")
        bq_silver = BigQuery("BigQuery Silver\n(Dados Tratados)")
        bq_gold = BigQuery("BigQuery Gold\n(Dados Curados)")
        
    with Cluster("Camada 5: Governança de Dados"):
        # Governança englobando todas as camadas
        dataplex = DataCatalog("Dataplex\n(Universal Catalog)")
        data_insights = BigQuery("Data Insights")
        
    with Cluster("Camada 6: Consumo e Visualização"):
        # Apresentação e Consumo Analítico
        powerbi = Client("Power BI")
        looker = DataStudio("Looker Studio")
        users = Users("Usuários Finais")

    # -----------------------------------------------------------
    # REGRAS DE FLUXO DE DADOS
    # -----------------------------------------------------------

    # Fluxo: Camada 1 -> Camada 2
    [sql_server, sap_bw] >> Edge(label="Conexão Restrita") >> vpn
    
    # Fluxo: Interno Camada 2
    vpn >> Edge(label="Tráfego Seguro") >> airflow
    vpn >> gcs
    airflow >> Edge(label="Orquestra") >> [gcs, pyspark_ingest]
    
    # Fluxo: Camada 2 -> Camada 4 (Ingestão Direta para Bronze)
    gcs >> Edge(label="Carga") >> bq_bronze
    pyspark_ingest >> Edge(label="Ingestão Batch") >> bq_bronze
    
    # Fluxo: Interação entre Camada 3 e Camada 4 (Processamento e Armazenamento)
    # Diretriz: FLUXO RETRÓGRADO (L4 para L3 visualmente). Utilizando dir="back"
    bq_pipelines >> Edge(dir="back", color="blue", label="Lê") >> bq_bronze
    bq_pipelines >> Edge(dir="forward", color="green", label="Grava") >> bq_silver
    
    bq_pipelines >> Edge(dir="back", color="blue", label="Lê") >> bq_silver
    bq_pipelines >> Edge(dir="forward", color="green", label="Grava") >> bq_gold
    
    # Outros engines interagindo com as camadas Medalhão (Leitura/Escrita)
    runtime >> Edge(dir="both", style="dotted", color="gray") >> bq_bronze
    spark_proc >> Edge(dir="both", style="dotted", color="gray") >> bq_silver
    notebook >> Edge(dir="both", style="dotted", color="gray") >> bq_silver
    sql_script >> Edge(dir="both", style="dotted", color="gray") >> bq_silver

    # Fluxo: Governança englobando o BQ
    # Conexões invisíveis ou direcionadas sutilmente para mostrar Governança (L4 -> L5)
    bq_bronze >> Edge(style="dashed", color="purple", dir="none") >> dataplex
    bq_silver >> Edge(style="dashed", color="purple", dir="none") >> dataplex
    bq_gold >> Edge(style="dashed", color="purple", dir="none") >> dataplex
    dataplex >> Edge(style="dashed", color="purple", dir="none") >> data_insights
    
    # Fluxo: Camada 4 -> Camada 6 (Consumo Gold)
    bq_gold >> Edge(label="Consumo Analítico") >> powerbi
    bq_gold >> Edge(label="Consumo Analítico") >> looker
    
    powerbi >> users
    looker >> users

    # -----------------------------------------------------------
    # DIRETRIZ: CONTROLE DE RANKING (A ESPINHA DORSAL INVISÍVEL)
    # -----------------------------------------------------------
    # Previne que o Graphviz embaralhe as posições lógicas das camadas.
    # Garante a progressão L1 -> L2 -> L3 -> L4 -> L5 -> L6
    (
        sql_server 
        >> Edge(style="invis") 
        >> vpn 
        >> Edge(style="invis") 
        >> bq_pipelines 
        >> Edge(style="invis") 
        >> bq_bronze 
        >> Edge(style="invis") 
        >> dataplex 
        >> Edge(style="invis") 
        >> looker
    )

# -----------------------------------------------------------
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO
# -----------------------------------------------------------
# Dependências necessárias (Linux/Mac/Windows)
# 1. Instale o Graphviz no S.O. (ex: sudo apt install graphviz ou brew install graphviz)
# 2. pip install diagrams
# 
# Para executar este script:
# python nome_do_arquivo.py
# -----------------------------------------------------------