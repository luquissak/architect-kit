import os
import sys
from diagrams import Diagram, Cluster, Edge

# Componentes GCP e Parceiros/Gerais
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery, Dataprep, Dataflow, Dataproc
from diagrams.gcp.storage import Storage as GCS
from diagrams.gcp.api import APIGateway
from diagrams.gcp.compute import Run
from diagrams.gcp.database import Spanner
from diagrams.gcp.analytics import Pubsub
from diagrams.gcp.operations import Monitoring
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage

# Garante o carregamento dos atributos visuais padronizados
# Adiciona o diretório backend ao path para encontrar common_attr.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend')))
try:
    from common_attr import graph_attr
except ImportError:
    graph_attr = {
        "fontname": "Arial",
        "fontsize": "20",
        "ranksep": "1.0",
        "nodesep": "0.6",
        "pad": "0.4",
        "splines": "ortho",
        "dpi": "600"
    }

# Força DPI 600 se não estiver definido ou se for menor
graph_attr["dpi"] = "600"

with Diagram("Plataforma MLOps SIPML - Referência Gartner v2", show=False, direction="LR", graph_attr=graph_attr, outformat="png"):

    # =========================================================================
    # 1. FONTES EXTERNAS DE DADOS
    # =========================================================================
    with Cluster("Fontes Externas de Dados"):
        with Cluster("Dados Analíticos (P&D)"):
            databricks = SQL("Azure Databricks\n(Delta Lake)")
            
        with Cluster("Dados Operacionais (Produção)"):
            on_prem = SQL("SIARA / On-Premises\n(IBM Db2 / Files)")
            external_apis = Storage("APIs Externas\n(Bacen / Serasa)")

    # =========================================================================
    # 2. SPOKE DE MODELAGEM (M) - FLUXO SUPERIOR
    # =========================================================================
    with Cluster("Spoke de Modelagem (Ciclo de Vida Analítico)"):
        with Cluster("M1: Sandbox e Ingestão"):
            bq_sandbox = BigQuery("BigQuery\n(Sandbox)")
            gcs_raw = GCS("Cloud Storage\n(Raw Data)")
            workbench = AIPlatform("Vertex AI Workbench\n(Notebooks)")

        with Cluster("M2: Orquestração MLOps (Vertex AI Pipelines)"):
            transformation = Dataflow("Dataflow / Dataproc\n(Feature Engineering)")
            custom_training = AIPlatform("Custom Training Jobs\n(Experiments & Tuning)")

        with Cluster("M3: Registro de Modelos"):
            model_registry = AIPlatform("Vertex AI\nModel Registry")

    # =========================================================================
    # 3. SPOKE DE INFERÊNCIA (I) - FLUXO INFERIOR
    # =========================================================================
    with Cluster("Spoke de Inferência (Ciclo de Vida Operacional)"):
        with Cluster("I1: Ingestão e Entrada"):
            api_gateway = APIGateway("Cloud API Gateway")
            pubsub = Pubsub("Pub/Sub\n(Streaming)")
            business_rules = Run("Cloud Run\n(Business Rules)")

        with Cluster("I2: Armazenamento e Features"):
            # Conforme solicitado: Feature explicitamente no BQ
            bq_features = BigQuery("BigQuery\n(Repositório de Features)") 
            spanner = Spanner("Cloud Spanner\n(Estado/Transacional)")

        with Cluster("I3: Serving e Inferência"):
            endpoint = AIPlatform("Vertex AI\nEndpoint de Inferência")

        with Cluster("I4: Observabilidade"):
            model_monitoring = Monitoring("Model Monitoring\n(Métricas e Drift)")
            bq_logs = BigQuery("BigQuery\n(Logs Operacionais)")

    # =========================================================================
    # 4. GOVERNANÇA TRANSVERSAL
    # =========================================================================
    with Cluster("Governança Enterprise"):
        dataplex = Dataprep("Dataplex (Data Mesh)\nLineage & Qualidade")

    # =========================================================================
    # ESPINHA DORSAL INVISÍVEL (Garante o alinhamento das colunas por empilhamento)
    # =========================================================================
    databricks >> Edge(style="invis") >> bq_sandbox >> Edge(style="invis") >> transformation >> Edge(style="invis") >> model_registry
    on_prem >> Edge(style="invis") >> api_gateway >> Edge(style="invis") >> bq_features >> Edge(style="invis") >> endpoint >> Edge(style="invis") >> dataplex

    # =========================================================================
    # RELAÇÕES E FLUXOS REAIS DE DADOS
    # =========================================================================
    
    # Fluxo Analítico / Modelagem
    databricks >> Edge(color="blue", label="Carga P&D") >> bq_sandbox
    gcs_raw >> workbench
    bq_sandbox >> workbench
    workbench >> Edge(color="blue", label="Trigger Pipeline") >> transformation
    transformation >> custom_training
    custom_training >> Edge(color="blue", label="Promove Modelo") >> model_registry

    # Integração Crítica: Modelagem publica as Features processadas diretamente no BQ do Spoke de Inferência
    transformation >> Edge(color="darkblue", style="dashed", label="Publica Features") >> bq_features

    # Fluxo Operacional / Inferência
    on_prem >> api_gateway
    external_apis >> api_gateway
    on_prem >> pubsub
    
    api_gateway >> business_rules
    pubsub >> business_rules
    
    # Serving consumindo modelo homologado e buscando features no BQ
    model_registry >> Edge(color="black", style="solid", label="Deploy") >> endpoint
    bq_features >> Edge(color="black", style="dashed", dir="back", label="Lookup") >> endpoint
    business_rules >> Edge(color="black", label="Request") >> endpoint
    
    # Telemetria e Logs
    endpoint >> model_monitoring
    model_monitoring >> bq_logs

    # Fluxos de Governança e Metadados (Dataplex coletando de todos os ambientes analíticos)
    bq_sandbox >> Edge(style="dashed", color="darkgreen") >> dataplex
    bq_features >> Edge(style="dashed", color="darkgreen") >> dataplex
    bq_logs >> Edge(style="dashed", color="darkgreen") >> dataplex
