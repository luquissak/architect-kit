import sys
import os
from diagrams import Diagram, Cluster, Edge

# IMPORT CRÍTICO DE ATRIBUTOS COMUNS (Regra Obrigatória)
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Imports corretos da biblioteca diagrams para GCP, Azure, OnPrem e Genéricos
from diagrams.azure.analytics import Databricks
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage as GenStorage
from diagrams.generic.network import Subnet
from diagrams.gcp.analytics import BigQuery, Dataproc, Dataflow, PubSub, DataCatalog
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform, MachineLearning
from diagrams.gcp.api import APIGateway
from diagrams.gcp.compute import Run
from diagrams.gcp.database import Spanner
from diagrams.gcp.operations import Monitoring

# Aplicando diretriz visual de linhas ortogonais aos atributos
graph_attr["splines"] = "ortho"

# Criação do diagrama com as configurações mandatórias
with Diagram("Plataforma MLOps - SIPML", show=False, direction="LR", graph_attr=graph_attr):

    # Definição de estilos de fluxo baseados na abstração de cores pedida
    fluxo_analitico = Edge(color="blue", style="solid")
    fluxo_producao = Edge(color="black", style="solid")
    fluxo_governanca = Edge(color="darkgreen", style="dashed")
    espinha_dorsal = Edge(style="invis")  # Conexões ocultas para forçar simetria

    # 1. BLOCO ESQUERDO: Fontes de Dados Externas
    with Cluster("Fontes de Dados Externas"):
        with Cluster("Dados Analíticos"):
            databricks = Databricks("Azure Databricks\n(Delta Lake)")

        with Cluster("Dados Operacionais"):
            db2 = SQL("IBM Db2\n(On-Prem)")
            file_storage = GenStorage("File Storage\n(On-Prem)")
            apis_bc = Subnet("APIs\n(Banco Central/Serasa)")

    # 2. BLOCO CENTRAL SUPERIOR: Spoke de Modelagem e P&D
    with Cluster("Spoke de Modelagem e P&D"):
        with Cluster("M1: Ingestão e P&D"):
            bq_sandbox = BigQuery("BigQuery\n(Sandbox)")
            gcs_raw = Storage("Cloud Storage\n(Raw Data)")
            workbench = AIPlatform("Vertex AI\nWorkbench")

        with Cluster("M2: Orquestração MLOps"):
            with Cluster("Vertex AI Pipelines"):
                dataproc = Dataproc("Dataproc\n(Transformações)")
                dataflow = Dataflow("Dataflow\n(Transformações)")
                custom_training = MachineLearning("Vertex AI Custom Training\n(ML Experiments & Tuning)")

        with Cluster("M3: Registro de Modelos"):
            model_registry = AIPlatform("Vertex AI\nModel Registry")

    # 3. BLOCO CENTRAL INFERIOR: Spoke de Inferência e Serving
    with Cluster("Spoke de Inferência e Serving"):
        with Cluster("I1: Ingestão e Entrada"):
            api_gw = APIGateway("Cloud API Gateway")
            cloud_run = Run("Cloud Run\n(Regras de Negócio)")
            pubsub = PubSub("Pub/Sub\n(Streaming)")

        with Cluster("I2: Armazenamento Técnico"):
            bq_feature_store = BigQuery("BigQuery\n(Repositório Features)")
            spanner = Spanner("Cloud Spanner")

        with Cluster("I3: Serving e Execução"):
            vertex_endpoint = AIPlatform("Vertex AI Endpoint\n(Online/Batch Prediction)")

        with Cluster("I4: Observabilidade"):
            model_monitoring = Monitoring("Vertex AI\nModel Monitoring")
            bq_logs = BigQuery("BigQuery\n(Logs Operacionais)")

    # 4. BLOCO DIREITO TRANSVERSAL: Governança
    with Cluster("Governança Corporativa"):
        dataplex = DataCatalog("Dataplex\n(Catálogo, Qualidade, Linhagem)")

    # -------------------------------------------------------------------------
    # MAPEAMENTO DE FLUXOS E CONEXÕES REAIS
    # -------------------------------------------------------------------------

    # Fontes para Modelagem
    databricks >> fluxo_analitico >> bq_sandbox

    # Fontes para Inferência (Operacional)
    db2 >> fluxo_producao >> api_gw
    file_storage >> fluxo_producao >> api_gw
    apis_bc >> fluxo_producao >> pubsub

    # Fluxo Interno: Spoke de Modelagem (Engajamento e P&D)
    workbench >> fluxo_analitico >> custom_training
    workbench >> fluxo_analitico >> dataproc
    workbench >> fluxo_analitico >> dataflow
    
    # Promoção do Modelo Treinado
    custom_training >> fluxo_analitico >> model_registry

    # Pipeline de Transformação de Features (Modelagem -> Inferência)
    dataproc >> fluxo_analitico >> bq_feature_store
    dataflow >> fluxo_analitico >> bq_feature_store

    # Fluxo Interno: Spoke de Inferência (Consumo)
    api_gw >> fluxo_producao >> cloud_run
    pubsub >> fluxo_producao >> cloud_run
    cloud_run >> fluxo_producao >> vertex_endpoint

    # Endpoint consome features e gera telemetria
    bq_feature_store >> fluxo_producao >> vertex_endpoint
    vertex_endpoint >> fluxo_producao >> model_monitoring
    model_monitoring >> fluxo_producao >> bq_logs

    # Fluxo de Governança (Monitoramento de Repositórios)
    dataplex >> fluxo_governanca >> bq_sandbox
    dataplex >> fluxo_governanca >> bq_feature_store
    dataplex >> fluxo_governanca >> bq_logs

    # -------------------------------------------------------------------------
    # ESPINHA DORSAL INVISÍVEL (Travamento e Alinhamento Ortogonal)
    # -------------------------------------------------------------------------
    
    # Travamento Vertical dos Líderes de Camada (para garantir ordem de renderização)
    bq_sandbox - espinha_dorsal - gcs_raw - espinha_dorsal - workbench
    dataproc - espinha_dorsal - dataflow - espinha_dorsal - custom_training
    api_gw - espinha_dorsal - cloud_run - espinha_dorsal - pubsub
    bq_feature_store - espinha_dorsal - spanner
    model_monitoring - espinha_dorsal - bq_logs

    # Travamento Horizontal das Colunas (Modelagem x Inferência)
    bq_sandbox - espinha_dorsal - api_gw
    dataproc - espinha_dorsal - bq_feature_store
    model_registry - espinha_dorsal - vertex_endpoint - espinha_dorsal - model_monitoring

# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO
# ==============================================================================
# Para rodar este script, você precisará do Graphviz e da biblioteca Diagrams.
# 
# 1. Instale o Graphviz no sistema operacional (ex: 'brew install graphviz' ou 'apt-get install graphviz')
# 2. Instale a biblioteca Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_arquivo.py
# ==============================================================================