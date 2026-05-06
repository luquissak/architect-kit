import os
import sys
from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery, Dataprep
from diagrams.gcp.operations import Monitoring

# Import obrigatório conforme a instrução crítica
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Inicialização do diagrama com layout da esquerda para a direita (Left to Right)
with Diagram("Arquitetura Spoke de Inferência SIPML", show=False, direction="LR", graph_attr=graph_attr):

    # 5. Camada Base de Governança (Transversal - posicionada à direita no fluxo final)
    with Cluster("Camada 5: Governança Transversal"):
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

    # ==========================================
    # Relações e Fluxos de Dados Reais
    # O alinhamento invisível incorreto foi removido para evitar 
    # que a seta da Camada 1 para a Camada 2 salte por cima da Camada 3.
    # O layout orgânico do Graphviz organizará Camada 1 e 3 paralelas antes da 2.
    # ==========================================
    
    # Model Registry (Camada 1) alimenta o Endpoint de inferência (Camada 2)
    model_registry >> endpoint

    # Repositório de Features (Camada 3) alimenta o Endpoint (Camada 2)
    bq_features >> Edge(color="blue", style="dashed") >> endpoint

    # Endpoint (Camada 2) envia dados para o Monitoramento (Camada 4)
    endpoint >> model_monitoring

    # Monitoramento (Camada 4) despeja logs no BigQuery de Operações (Camada 4)
    model_monitoring >> bq_logs

    # Governança (Dataplex) monitora os repositórios BigQuery
    bq_features >> Edge(style="dashed", color="darkgreen") >> dataplex
    bq_logs >> Edge(style="dashed", color="darkgreen") >> dataplex

    # -----------------------------------------------------------
    # Instruções de instalação e execução
    # 
    # Para instalar as dependências necessárias, execute:
    # pip install diagrams
    # 
    # Para gerar o diagrama, execute este script:
    # python nome_do_arquivo.py
    # -----------------------------------------------------------