import os
import sys
from diagrams import Diagram, Cluster, Edge

# Importação obrigatória dos atributos comuns de grafo e injeção do diretório
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Importações de componentes da biblioteca diagrams
from diagrams.onprem.client import Users, Client
from diagrams.gcp.network import LoadBalancing, Armor, DNS
from diagrams.gcp.api import APIGateway
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.compute import Run
from diagrams.gcp.operations import Monitoring

# Configuração para forçar linhas ortogonais em ângulos de 90 graus (Diretriz Visual 2)
graph_attr.update({"splines": "ortho", "nodesep": "1.2", "ranksep": "1.5"})

with Diagram("MLOps Network - SIPML", show=False, direction="LR", graph_attr=graph_attr):

    # CAMADA COMPLEMENTAR: Origens de Tráfego (Borda Esquerda)
    with Cluster("Origens de Tráfego Externo"):
        users = Users("Usuários\n(Cientistas/Engenheiros)")
        apps = Client("Aplicações\nConsumidoras")

    # COLUNA 1: Spoke de Modelagem (Esquerda)
    with Cluster("Spoke de Modelagem\n(prj-sipml-modelagem-anl)"):
        workbench = AIPlatform("Vertex AI\nWorkbench")
        pipelines = AIPlatform("Vertex AI\nPipelines")
        bq_sandbox = BigQuery("BigQuery\n(Sandbox)")

        # Fluxo interno de desenvolvimento analítico
        workbench >> pipelines >> bq_sandbox

    # COLUNA 2: Hub Central (Centro)
    with Cluster("Hub Central de Orquestração\n(prj-sipml-gateway-prd)"):
        armor = Armor("Cloud Armor\n(WAF)")
        lb = LoadBalancing("Cloud Load\nBalancing")
        api_gw = APIGateway("API Gateway\n/ Apigee")
        dns_psc = DNS("Cloud DNS\n+ PSC")

        # Entrada unificada e orquestração
        armor >> lb >> api_gw
        # Resolução de DNS / Lookup Privado para os Spokes
        api_gw >> Edge(style="dashed", color="gray", label="Lookup Privado") >> dns_psc

    # COLUNA 3: Spoke de Inferência (Direita)
    with Cluster("Spoke de Inferência e Serving\n(prj-sipml-inferencia-prd)"):
        run_rules = Run("Cloud Run\n(Business Rules)")
        vertex_endpoint = AIPlatform("Vertex AI\nEndpoint")
        bq_features = BigQuery("BigQuery\n(Feature Store)")
        model_monitor = Monitoring("Vertex AI\nModel Monitoring")
        bq_logs = BigQuery("BigQuery\n(Logs)")

        # Fluxo de chamada online e telemetria
        run_rules >> vertex_endpoint
        vertex_endpoint >> bq_features
        vertex_endpoint >> model_monitor >> bq_logs

    # FLUXOS REAIS DE CONEXÃO (Interconectividade Hub-and-Spoke)
    
    # 1. Tráfego externo atinge o Hub Central na borda
    users >> armor
    apps >> armor

    # 2. API Gateway roteia para o Spoke de Modelagem (Desenvolvimento / Orquestração)
    api_gw >> Edge(label="Roteamento Dev\n(VPC Peering)", color="black", dir="forward") >> workbench

    # 3. API Gateway roteia para o Spoke de Inferência (Negócios / Serving)
    api_gw >> Edge(label="Roteamento Negócio\n(PSC)", color="black") >> run_rules

    # ESPINHA DORSAL INVISÍVEL: Trava estrutural para forçar o alinhamento em colunas (Diretriz Visual 4)
    # A ordem força: Origens -> Modelagem -> Hub -> Inferência
    users - Edge(style="invis") - workbench - Edge(style="invis") - armor - Edge(style="invis") - run_rules
    apps - Edge(style="invis") - bq_sandbox - Edge(style="invis") - api_gw - Edge(style="invis") - bq_logs

# ==========================================
# INSTRUÇÕES PARA EXECUÇÃO DO SCRIPT
# ==========================================
# 1. Certifique-se de ter o Graphviz instalado no seu sistema operacional:
#    - Linux: sudo apt-get install graphviz
#    - Mac: brew install graphviz
#    - Windows: choco install graphviz
# 2. Instale a biblioteca Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_arquivo.py