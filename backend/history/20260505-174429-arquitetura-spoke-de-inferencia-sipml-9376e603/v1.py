import os
import sys
from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery, Dataprep
from diagrams.gcp.operations import Monitoring

# Import obrigatório conforme a instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Inicialização do diagrama com layout da esquerda para a direita e ocultação automática
with Diagram("Arquitetura Spoke de Inferência SIPML", show=False, direction="LR", graph_attr=graph_attr):

    # 5. Camada Base de Governança (Transversal)
    with Cluster("Camada 5: Governança Transversal"):
        # Ícone de Dataprep com descrição de Dataplex conforme diretrizes
        dataplex = Dataprep("Dataplex (Data Mesh)\nCatálogo, Qualidade\nMetadados e Linhagem")

    # Agrupamento lógico do projeto autônomo (Spoke)
    with Cluster("Projeto de Inferência (Spoke)"):

        # 1. Camada de Deploy de Modelos
        with Cluster("Camada 1: Deploy de Modelos"):
            model_registry = AIPlatform("Vertex AI\nModel Registry")

        # 3. Camada de Features para Serving
        with Cluster("Camada 3: Features para Serving"):
            bq_features = BigQuery("BigQuery\n(Repositório de Features)")

        # 2. Camada de Serving
        with Cluster("Camada 2: Serving"):
            endpoint = AIPlatform("Vertex AI\nEndpoint de Inferência")

        # 4. Camada de Observabilidade
        with Cluster("Camada 4: Observabilidade"):
            model_monitoring = Monitoring("Model Monitoring\n(Métricas e Drift)")
            bq_logs = BigQuery("BigQuery\n(Logs e Métricas Operacionais)")

    # Relações e Fluxos de Dados
    
    # Model Registry -> Endpoint (Deploy de modelos homologados)
    model_registry >> Edge(label="Deploy") >> endpoint

    # Endpoint -> BigQuery (Consulta de features para predição)
    endpoint >> Edge(label="Consulta de Features") >> bq_features

    # Endpoint -> Model Monitoring (Envio de métricas de performance e drift)
    endpoint >> Edge(label="Métricas/Drift") >> model_monitoring

    # Model Monitoring -> BigQuery (Persistência dos logs operacionais e métricas)
    model_monitoring >> Edge(label="Persistência") >> bq_logs

    # BigQuery -> Dataplex (Atuação da Governança nos repositórios)
    bq_features >> Edge(label="Governança/Catálogo", style="dashed", color="darkgreen") >> dataplex
    bq_logs >> Edge(label="Governança/Catálogo", style="dashed", color="darkgreen") >> dataplex

# -----------------------------------------------------------
# Instruções de instalação e execução
# 
# Para instalar as dependências necessárias, execute:
# pip install diagrams
# 
# Para gerar o diagrama, execute este script:
# python nome_do_arquivo.py
# -----------------------------------------------------------