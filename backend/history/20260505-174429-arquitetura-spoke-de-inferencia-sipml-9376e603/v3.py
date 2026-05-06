from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery, Dataprep
from diagrams.gcp.operations import Monitoring
import os
import sys

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

        # 3. Camada de Features para Serving (Movida logicamente para antes do Serving no fluxo)
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
    # TRICK DE ALINHAMENTO: Fluxo Invisível de Camadas
    # Force o Graphviz a ordenar as camadas da esquerda para a direita
    # ==========================================
    model_registry >> Edge(style="invis") >> bq_features >> Edge(style="invis") >> endpoint >> Edge(style="invis") >> model_monitoring >> Edge(style="invis") >> dataplex

    # ==========================================
    # Relações e Fluxos de Dados Reais
    # ==========================================
    
    # Model Registry alimenta o Endpoint de inferência
    model_registry >> endpoint

    # Endpoint consome dados do Repositório de Features (Seta invertida visualmente para manter o alinhamento da esquerda para a direita)
    bq_features >> Edge(color="blue", style="dashed") >> endpoint

    # Endpoint envia dados para o Monitoramento
    endpoint >> model_monitoring

    # Monitoramento despeja logs no BigQuery de Operações (agrupados no mesmo nível/cluster)
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