from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import Bigquery, DataCatalog
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform
import os
import sys

# Importação obrigatória dos atributos de grafo compartilhados
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Configuração de linhas ortogonais (ângulos de 90 graus)
graph_attr["splines"] = "ortho"

# Criação do diagrama sem exibir automaticamente e alinhado da Esquerda para a Direita
with Diagram("prj-modelagem-ab-Spoke", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada 1: Ingestão e Sandbox (Extrema Esquerda)
    with Cluster("Camada 1: Ingestão e Sandbox"):
        bq_sandbox = Bigquery("BigQuery\n(Sandbox)")
        gcs_raw = Storage("Cloud Storage\n(Raw Data)")
        workbench = AIPlatform("Vertex AI Workbench\n(Notebooks)")
        
        # Fluxo interno da Camada 1
        bq_sandbox >> workbench
        gcs_raw >> workbench

    # Camada 2: Orquestração de MLOps (Central)
    with Cluster("Camada 2: Vertex AI Pipelines (MLOps)"):
        feature_store = AIPlatform("Feature Store")
        model_training = AIPlatform("Model Training")
        evaluation = AIPlatform("Evaluation")
        
        # Fluxo sequencial interno da Camada 2
        feature_store >> model_training >> evaluation

    # Camada 3: Destinos e Governança (Extrema Direita)
    with Cluster("Camada 3: Destinos e Governança"):
        with Cluster("Governança"):
            dataplex = DataCatalog("Dataplex")
            
        model_registry = AIPlatform("Model Registry\n(Candidato Homologado)")

    # Conexões explícitas entre camadas
    workbench >> Edge(label="Trigger Pipeline") >> feature_store
    evaluation >> model_registry
    
    # A Espinha Dorsal Invisível: controle de ranking para travar as colunas
    # Isso impede que o Graphviz embaralhe as posições lógicas do diagrama
    workbench >> Edge(style="invis") >> feature_store >> Edge(style="invis") >> model_registry

    # =========================================================================
    # INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
    # 1. Instale a biblioteca diagrams e o graphviz no sistema:
    #    pip install diagrams
    #    (Requer Graphviz instalado no S.O.: apt-get install graphviz ou choco install graphviz)
    # 2. Execute este script:
    #    python nome_do_arquivo.py
    # =========================================================================